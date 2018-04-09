from flask import Flask, render_template, request, url_for, redirect, session
import config
from exts import db
from models import *
import urllib
import json

app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)

# Create all tables;
# with app.app_context():
#     db.create_all()

@app.route('/')
def home():
    if session.get('username') is None:
        return render_template('home.html')
    else:
        return redirect(url_for('dashboard'))

@app.route('/dashboard/', methods=['GET', 'POST'])
def dashboard():
    username = session.get('username')
    if username is None:
        return render_template('home.html')
    else:
        url = "http://cs9900fafafa.azurewebsites.net/api/User/GetUserProfile?username="+username
        response = urllib.urlopen(url)
        profileInfo = json.loads(response.read())
        return render_template('dashboard.html', result=username)

@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        username = request.form.get('username')
        password = request.form.get('password')
        url = "http://cs9900fafafa.azurewebsites.net/api/User/login?username="+username+"&password="+password
        response = urllib.urlopen(url)
        password_check = json.loads(response.read())["Login Status"]
        if password_check == "Success":
            session['username'] = username
            return redirect(url_for('dashboard'))
        else:
            return 'Wrong password'

@app.route('/register/', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    else:
        username = request.form.get('username')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        if password1 != password2:
            return 'Password confirmation error'
        else:
            url = "http://cs9900fafafa.azurewebsites.net/api/User/Register?username="+username+"&password="+password1
            response = urllib.urlopen(url)
            userExisted = json.loads(response.read())
            if userExisted["Create User Status"] == "Fail":
                return 'User existed'
            else:
                return render_template("login.html")

@app.route('/stockbasic/', methods=['POST'])
def stockbasicinfo():
    stockid = request.form.get('stockid')
    if session.get('username') is None:
        return render_template('stockbasic.html', result=stockid)
    else:
        return render_template('stockbasiclogin.html', result=stockid)

@app.route('/stockfull/', methods=['POST'])
def stockfullinfo():
    stockid = request.form.get('stockid')
    url = "http://cs9900fafafa.azurewebsites.net/api/BasicInfo/GetBasicInfo?stockId="
    response = urllib.urlopen(url + stockid)
    stockInfos = json.loads(response.read())
    if session.get('username') is None:
        return render_template('stockinfo.html', result=stockInfos)
    else:
        return render_template('stockinfologin.html', result=stockInfos)

@app.route('/logout/', methods=['GET'])
def logout():
    session.pop('username')
    return render_template('home.html')

@app.route('/demo/')
def demo():
    return render_template('multipledemo.html')

# @app.route('/import/')
# def stock():
#     test_stock = Stock(ticker_symbol='AAPL', company='Apple')
#     db.session.add(test_stock)
#     db.session.commit()
#     return 'Import succeed!'

if __name__ == '__main__':
    app.run()
