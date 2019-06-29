from flask import Flask
from flask import render_template

app = Flask(__name__)

@app.route('/')
def index():
    return "index page"

@app.route('/hello')
def hello():
    return render_template('hello.html', name='User')

if __name__ == '__main__':
    app.run(debug=True)