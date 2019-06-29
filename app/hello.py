import os, json, config
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

class TwitterAccount:
    def isFollow(self, followee):
        pass

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
            print(True)
            flash(u'異なるユーザー同士を入力してください', 'alert alert-danger')
        return render_template('index.html', form = form)
    else:
        return render_template('index.html', form = form)

if __name__ == '__main__':
    app.run(debug=True)