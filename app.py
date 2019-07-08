import os
import json
from flask import Flask, render_template, request, flash, redirect, make_response
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from requests_oauthlib import OAuth1Session

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(32)
bootstrap = Bootstrap(app)

# ログインなしで利用する場合のTwitterAPI用トークン
CK = os.environ["CONSUMER_KEY"]
CS = os.environ["CONSUMER_SECRET"]
AT = os.environ["ACCESS_TOKEN"]
ATS = os.environ["ACCESS_TOKEN_SECRET"]

# URLs
base_url = 'https://api.twitter.com/'
base_json_url = base_url + '1.1/{}.json'
request_token_url = base_url + 'oauth/request_token'
authorization_url = base_url + 'oauth/authenticate'
access_token_url = base_url + 'oauth/access_token'


class TwitterUserAccountForm(FlaskForm):
    user_id_1 = StringField('ID', validators=[DataRequired()], render_kw={
                            "placeholder": "username"})
    user_id_2 = StringField('ID', validators=[DataRequired()], render_kw={
                            "placeholder": "username"})
    submit = SubmitField('Submit')


def FollowingCheck(user_id_1, user_id_2, twitter_session):
    followflags = {'user_id_1': 'False', 'user_id_2': 'False'}
    if isPublicAccount(user_id_1, twitter_session):
        relationship = isFollow(user_id_1, user_id_2, twitter_session)
        followflags["user_id_1"] = relationship[0]
        followflags["user_id_2"] = relationship[1]
        return followflags
    else:
        relationship = isFollow(user_id_2, user_id_1, twitter_session)
        followflags["user_id_1"] = relationship[1]
        followflags["user_id_2"] = relationship[0]
        return followflags


def isPublicAccount(user_id, twitter_session):
    endpoint = base_json_url.format('statuses/user_timeline')
    params = "screen_name=" + user_id + "&count=1"
    res = twitter_session.get(endpoint, params=params)
    response = json.loads(res.text)
    if ("error" in response):
        return False
    return True


def isFollow(user_id_1, user_id_2, twitter_session):
    endpoint = base_json_url.format('friendships/show')
    params = "source_screen_name="+user_id_1+"&target_screen_name="+user_id_2
    res = twitter_session.get(endpoint, params=params)
    response = json.loads(res.text)
    is_user1_following = response['relationship']['source']['following']
    is_user2_following = response['relationship']['target']['following']
    return is_user1_following, is_user2_following  # boolean


def FollowingCheckInJapanese(followflag):
    if followflag == True:
        return "フォローしています"
    return "フォローしていません"


def isSameTwitterAccount(user_id_1, user_id_2):
    if user_id_1 == user_id_2:
        return True
    else:
        return False


def ValidateUserIds(user_id_1, user_id_2, twitter_session):
    if isSameTwitterAccount(user_id_1, user_id_2):
        return "異なるユーザー同士を入力してください"
    elif (not isPublicAccount(user_id_1, twitter_session)) and (not isPublicAccount(user_id_2, twitter_session)):
        return "確認できませんでした（どちらかのアカウントにログインしてください）"


def check_result(user_id_1, user_id_2, twitter_session):
    followflags = FollowingCheck(user_id_1, user_id_2, twitter_session)
    message1 = "@" + user_id_1 + " は @" + user_id_2 + " を" + \
        FollowingCheckInJapanese(followflags['user_id_1'])
    message2 = "@" + user_id_2 + " は @" + user_id_1 + " を" + \
        FollowingCheckInJapanese(followflags['user_id_2'])
    return message1, message2


def setTwitterSession():
    access_token = request.cookies.get('oauth_token', AT)
    access_token_secret = request.cookies.get('oauth_token_secret', ATS)
    twitter_session = OAuth1Session(CK, CS, access_token, access_token_secret)
    return twitter_session


@app.route('/', methods=["GET", "POST"])
def index():
    form = TwitterUserAccountForm(request.form)
    twitter_session = setTwitterSession()
    if request.method == 'POST':
        user_id_1 = request.form['user_id_1']
        user_id_2 = request.form['user_id_2']
        validate_result = ValidateUserIds(
            user_id_1, user_id_2, twitter_session)
        if validate_result is not None:
            flash(validate_result, 'alert alert-danger')
            return render_template('index.html', form=form)
        else:
            message1, message2 = check_result(
                user_id_1, user_id_2, twitter_session)
            return render_template('index.html', form=form, results=[message1, message2])
    else:
        return render_template('index.html', form=form)


@app.route('/login', methods=["GET"])
def login():
    twitter = OAuth1Session(CK, CS)
    twitter.fetch_request_token(request_token_url)
    auth_url = twitter.authorization_url(authorization_url)
    return redirect(auth_url)


@app.route('/callback', methods=["GET"])
def callback():
    # アクセストークンをTwitterから取得
    redirect_response = request.url
    twitter = OAuth1Session(CK, CS)
    twitter.parse_authorization_response(redirect_response)
    res = twitter.fetch_access_token(access_token_url)

    # アクセストークンを取り出す
    loginuser_access_token = res.get('oauth_token')
    loginuser_access_token_secret = res.get('oauth_token_secret')

    # トークンをcookieにセットしてrootパスにリダイレクト
    redirect_to_index = app.make_response(redirect('/'))
    redirect_to_index.set_cookie('oauth_token', value = loginuser_access_token)
    redirect_to_index.set_cookie('oauth_token_secret', value = loginuser_access_token_secret)
    return redirect_to_index


@app.route('/logout', methods=["GET"])
def logout():
    # まだ具体的な処理は入れてない
    form = TwitterUserAccountForm(request.form)
    flash(u'ログアウトしました', 'alert alert-success')
    return render_template('index.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)
