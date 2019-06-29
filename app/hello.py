import os
from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)

bootstrap = Bootstrap(app)
app.config['SECRET_KEY'] = os.urandom(32)

class TwitterUserAccount(FlaskForm):
    user_id_1 = StringField('ID', validators=[DataRequired()])
    user_id_2 = StringField('ID', validators=[DataRequired()])
    submit = SubmitField('Submit')

@app.route('/', methods = ["GET", "POST"])
def index():
    form = TwitterUserAccount(request.form)
    if request.method == 'POST':
        user_id_1 = request.form['user_id_1']
        user_id_2 = request.form['user_id_2']
        return render_template('index.html', form = form)
    else:
        return render_template('index.html', form = form)

@app.route('/hello')
def hello():
    return render_template('hello.html', name='User')

if __name__ == '__main__':
    app.run(debug=True)