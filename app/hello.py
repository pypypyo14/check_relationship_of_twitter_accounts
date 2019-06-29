import os
from flask import Flask, render_template, request, flash
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)

bootstrap = Bootstrap(app)
app.config['SECRET_KEY'] = os.urandom(32)

class TwitterUserAccount(FlaskForm):
    user_id_1 = StringField('ID', validators=[DataRequired()], render_kw={"placeholder": "username"})
    user_id_2 = StringField('ID', validators=[DataRequired()], render_kw={"placeholder": "username"})
    submit = SubmitField('Submit')

def FollowingCheck(user_id_1, user_id_2):
    followflags={'User1followUser2':'0', 'User2followUser1':'0'}
    if isFollow(user_id_1, user_id_2):
        followflags["User1followUser2"] = 1
    if isFollow(user_id_2, user_id_1):
        followflags["User2followUser1"] = 1
    return followflags

def isFollow(follower, followee):
        pass

def FollowingCheckInJapanese(followflag):
    print(followflag)
    if followflag == 1:
        return "います"
    return "いません"

def isSameTwitterAccount(user_id_1, user_id_2):
    if user_id_1 == user_id_2:
        return True
    else:
        return False

@app.route('/', methods = ["GET", "POST"])
def index():
    form = TwitterUserAccount(request.form)
    if request.method == 'POST':
        user_id_1 = request.form['user_id_1']
        user_id_2 = request.form['user_id_2']
        if isSameTwitterAccount(user_id_1, user_id_2):
            flash(u'異なるユーザー同士を入力してください', 'alert alert-danger')
            return render_template('index.html', form = form)
        else:
            followflags = FollowingCheck(user_id_1, user_id_2)
            message1 = "@" + user_id_1 + " は @" + user_id_2 + " をフォローして" + FollowingCheckInJapanese(followflags['User1followUser2'])
            message2 = "@" + user_id_2 +  "は @" + user_id_1 + " をフォローして" + FollowingCheckInJapanese(followflags['User2followUser1'])
            return render_template('index.html', form = form, results = [message1, message2])
    else:
        return render_template('index.html', form = form)

if __name__ == '__main__':
    app.run(debug=True)