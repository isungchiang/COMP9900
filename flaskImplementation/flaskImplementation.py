from flask import Flask, render_template, request, url_for, redirect, session
import config
import urllib
import json

app = Flask(__name__)
app.config.from_object(config)

@app.route('/')
def home():
    if session.get('username') is None:
        return render_template('home.html')
    else:
        return redirect(url_for('dashboard'))

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    username = session.get('username')
    if username is None:
        return render_template('home.html')
    else:
        return render_template('userprofile.html', username=username)

@app.route('/login', methods=['GET', 'POST'])
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

@app.route('/register', methods=['GET', 'POST'])
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

@app.route('/stockbasic', methods=['POST'])
def stockbasicinfo():
    stockid = request.form.get('stockid')
    username = session.get('username')
    if username is None:
        return render_template('stockbasic.html', stockid=stockid)
    else:
        return render_template('stockbasiclogin.html', stockid=stockid, username=username)

@app.route('/stockfull', methods=['POST'])
def stockfullinfo():
    stockid = request.form.get('stockid')
    url = "http://cs9900fafafa.azurewebsites.net/api/BasicInfo/GetBasicInfo?stockId="
    response = urllib.urlopen(url + stockid)
    stockInfos = json.loads(response.read())
    username = session.get('username')
    if username is None:
        return render_template('stockinfo.html', result=stockInfos)
    else:
        return render_template('stockinfologin.html', result=stockInfos, username=username)

@app.route('/logout', methods=['GET'])
def logout():
    session.pop('username')
    return render_template('home.html')

@app.route('/portfolio')
def portfolio():
    username = session.get('username')
    if username is None:
        return render_template('home.html')
    else:
        portfolioname = request.args.get('portfolioname')
        return render_template('portfolioinfo.html', username=username, portfolio=portfolioname)

@app.route('/createportfolio', methods=['GET', 'POST'])
def createportfolio():
    username = session.get('username')
    if username is None:
        return render_template('home.html')
    else:
        if request.method == 'GET':
            return render_template('createportfolio.html', username=username)
        else:
            portfolioname = request.form.get('portfolioname')
            url = "http://cs9900fafafa.azurewebsites.net/api/Portfolio/AddPortfolio?username="+username+"&portfolioname="+portfolioname
            response = urllib.urlopen(url)
            portfolioExisted = json.loads(response.read())["Create portfolio Status"]
            if portfolioExisted == "Success":
                return render_template('userprofile.html', username=username)
            else:
                return "Create Portfolio Failed"

@app.route('/profile')
def profile():
    username = session.get('username')
    if username is None:
        return render_template('home.html')
    else:
        return render_template('userprofile.html', username=username)

@app.route('/addtransaction', methods=['GET', 'POST'])
def addtransaction():
    username = session.get('username')
    if username is None:
        return render_template('home.html')
    else:
        if request.method == 'GET':
            return render_template('addtransaction.html', username=username)
        else:
            portfolioname = request.form.get('portfolioname')
            stockid = request.form.get('stockid')
            shares = request.form.get('shares')
            tradedate = request.form.get('tradedate')
            tradeprice = request.form.get('tradeprice')
            url = "http://cs9900fafafa.azurewebsites.net/api/Portfolio/CreateTransaction?username="+username+"&portfolioname="+portfolioname+"&StockId="+stockid+"&Shares="+shares+"&TradeDate="+tradedate+"&TradePrice="+tradeprice
            response = urllib.urlopen(url)
            transactionStatus = json.loads(response.read())["Create Transaction Status"]
            if transactionStatus == "Success":
                return render_template('portfolioinfo.html', username=username, portfolio=portfolioname)
            else:
                return "Add transaction Failed."

if __name__ == '__main__':
    app.run()
