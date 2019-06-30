import os, json
from flask import Flask, render_template, request, flash
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from requests_oauthlib import OAuth1Session

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(32)
bootstrap = Bootstrap(app)

CK = os.environ["CONSUMER_KEY"]
CS = os.environ["CONSUMER_SECRET"]
AT = os.environ["ACCESS_TOKEN"]
ATS = os.environ["ACCESS_TOKEN_SECRET"]
twitter = OAuth1Session(CK, CS, AT, ATS)

class TwitterUserAccountForm(FlaskForm):
    user_id_1 = StringField('ID', validators=[DataRequired()], render_kw={"placeholder": "username"})
    user_id_2 = StringField('ID', validators=[DataRequired()], render_kw={"placeholder": "username"})
    submit = SubmitField('Submit')

def FollowingCheck(user_id_1, user_id_2):
    followflags={'user_id_1':'False', 'user_id_2':'False'}
    if isPublicAccount(user_id_1):
        relationship = isFollow(user_id_1, user_id_2)
        followflags["user_id_1"] = relationship[0]
        followflags["user_id_2"] = relationship[1]
        return followflags
    else:
        relationship = isFollow(user_id_2, user_id_1)
        followflags["user_id_1"] = relationship[1]
        followflags["user_id_2"] = relationship[0]
        return followflags

def isPublicAccount(user_id):
    endpoint = "https://api.twitter.com/1.1/statuses/user_timeline.json"
    params = "screen_name=" + user_id +"&count=1"
    res = twitter.get(endpoint, params = params)
    response = json.loads(res.text)
    print(response)
    if ("error" in response):
        return False
    return True

def isFollow(user_id_1, user_id_2):
    endpoint = "https://api.twitter.com/1.1/friendships/show.json"
    params = "source_screen_name="+user_id_1+"&target_screen_name="+user_id_2
    res = twitter.get(endpoint, params = params)
    response = json.loads(res.text)
    print(response)
    is_user1_following = response['relationship']['source']['following']
    is_user2_following = response['relationship']['target']['following']
    return is_user1_following, is_user2_following

def FollowingCheckInJapanese(followflag):
    if followflag == True:
        return "います"
    return "いません"

def isSameTwitterAccount(user_id_1, user_id_2):
    if user_id_1 == user_id_2:
        return True
    else:
        return False

@app.route('/', methods = ["GET", "POST"])
def index():
    form = TwitterUserAccountForm(request.form)
    if request.method == 'POST':
        user_id_1 = request.form['user_id_1']
        user_id_2 = request.form['user_id_2']
        if isSameTwitterAccount(user_id_1, user_id_2):
            flash(u'異なるユーザー同士を入力してください', 'alert alert-danger')
            return render_template('index.html', form = form)
        if (not isPublicAccount(user_id_1)) and (not isPublicAccount(user_id_2)):
            flash(u'どちらも鍵垢さんのようです', 'alert alert-danger')
            return render_template('index.html', form = form)
        else:
            followflags = FollowingCheck(user_id_1, user_id_2)
            message1 = "@" + user_id_1 + " は @" + user_id_2 + " をフォローして" + FollowingCheckInJapanese(followflags['user_id_1'])
            message2 = "@" + user_id_2 + " は @" + user_id_1 + " をフォローして" + FollowingCheckInJapanese(followflags['user_id_2'])
            return render_template('index.html', form = form, results = [message1, message2])
    else:
        return render_template('index.html', form = form)

if __name__ == '__main__':
    app.run(debug=True)