from flask import Flask, render_template,request
import config
from exts import db
from models import User

app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/dashboard/', methods=['GET', 'POST'])
def dashboard():
    return render_template('dashboard.html')

@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        return render_template('dashboard.html')

@app.route('/register/', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    else:
        return render_template('dashboard.html')

if __name__ == '__main__':
    app.run()
