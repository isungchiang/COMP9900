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
        return render_template('usertransaction.html', username=username)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        username = request.form.get('username')
        password = request.form.get('password')
        url = "http://comp9900fafafa.azurewebsites.net/api/User/login?username="+username+"&password="+password
        response = urllib.urlopen(url)
        password_check = json.loads(response.read())["Login Status"]
        if password_check == "Success":
            session['username'] = username
            return redirect(url_for('usersummary'))
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
            url = "http://comp9900fafafa.azurewebsites.net/api/User/Register?username="+username+"&password="+password1
            response = urllib.urlopen(url)
            userExisted = json.loads(response.read())
            if userExisted["Create User Status"] == "Fail":
                return 'User existed'
            else:
                return redirect(url_for('login'))

@app.route('/stockbasic', methods=['GET', 'POST'])
def stockbasicinfo():
    if request.method == 'POST':
        stockid = request.form.get('stockid')
    else:
        stockid = request.args.get('stockid')
    stockid = str(stockid).upper()
    username = session.get('username')
    if username is None:
        return render_template('stockbasic.html', stockid=stockid)
    else:
        return render_template('stockbasiclogin.html', stockid=stockid, username=username)

@app.route('/stockfull', methods=['GET', 'POST'])
def stockfullinfo():
    if request.method == 'POST':
        stockid = request.form.get('stockid')
    else:
        stockid = request.args.get('stockid')
    stockid = str(stockid).upper()
    url = "http://comp9900fafafa.azurewebsites.net/api/BasicInfo/GetBasicInfo?stockId="
    response = urllib.urlopen(url + stockid)
    stockInfos = json.loads(response.read())

    url = 'http://comp9900fafafa.azurewebsites.net/api/BasicInfo/GetStat?stockId='
    response = urllib.urlopen(url + stockid)
    read = response.read()
    marks = json.loads(read)
    refresh_date = []
    content = []
    try:
        detail = marks[0]['json']
        detail = str(detail).replace('\'', '\"')
        detail = json.loads(detail, encoding='utf-8')
        refresh_date.append(detail['last_refresh_date'])
        print(detail['marks'][detail['last_refresh_date']]['labels'])
        labels = detail['marks'][detail['last_refresh_date']]['labels']
        for i in labels:
            if labels[i]['labels']==0:
                content_ = '<strong style = "color: #d75442">'+ labels[i]['content']+'</strong>'
            else:
                content_ = '<strong style = "color: #69D694">' + labels[i]['content'] + '</strong>'
            content.append(content_)
    except:
        pass
    username = session.get('username')
    if username is None:
        return render_template('stockinfo.html', stockid=stockid, result=stockInfos, refresh_date=refresh_date,content=content)
    else:
        return render_template('stockinfologin.html', stockid=stockid, result=stockInfos, username=username, refresh_date=refresh_date,content=content)

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
        return render_template('portfoliotransactioninfo.html', username=username, portfolio=portfolioname)

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
            url = "http://comp9900fafafa.azurewebsites.net/api/Portfolio/AddPortfolio?username="+username+"&portfolioname="+portfolioname
            response = urllib.urlopen(url)
            portfolioExisted = json.loads(response.read())["Create portfolio Status"]
            if portfolioExisted == "Success":
                return render_template('usertransaction.html', username=username)
            else:
                return "Create Portfolio Failed"

@app.route('/deleteportfolio', methods=['GET'])
def deleteportfolio():
    username = session.get('username')
    if username is None:
        return render_template('home.html')
    else:
        portfolioname = request.args.get('portfolioname')
        url = "http://comp9900fafafa.azurewebsites.net/api/Portfolio/DeletePortfolio?username="+username+"&portfolioname="+portfolioname
        response = urllib.urlopen(url)
        portfolioExisted = json.loads(response.read())["Delete portfolio Status"]
        if portfolioExisted == "Success":
            return render_template('usertransaction.html', username=username)
        else:
            return "Delete Portfolio Failed"

@app.route('/addtransaction', methods=['GET', 'POST'])
def addtransaction():
    username = session.get('username')
    if username is None:
        return render_template('home.html')
    else:
        if request.method == 'GET':
            portfolioname = request.args.get('portfolioname')
            stockid = request.args.get('stockid')
            stockid = str(stockid).upper()
            return render_template('addtransaction.html', username=username, portfolio=portfolioname, stockid=stockid)
        else:
            portfolioname = request.form.get('portfolioname')
            stockid = request.form.get('stockid')
            stockid = str(stockid).upper()
            shares = request.form.get('shares')
            tradedate = request.form.get('tradedate')
            tradeprice = request.form.get('tradeprice')
            url = "http://comp9900fafafa.azurewebsites.net/api/Portfolio/CreateTransaction?username="+username+"&portfolioname="+portfolioname+"&StockId="+stockid+"&Shares="+shares+"&TradeDate="+tradedate+"&TradePrice="+tradeprice
            response = urllib.urlopen(url)
            transactionStatus = json.loads(response.read())["Create Transaction Status"]
            if transactionStatus == "Success":
                return render_template('portfoliotransactioninfo.html', username=username, portfolio=portfolioname)
            else:
                return "Add transaction Failed."

@app.route('/deletetransaction', methods=['GET'])
def deletetransaction():
    username = session.get('username')
    if username is None:
        return render_template('home.html')
    else:
        portfolioname = request.args.get('Portfolioname')
        stockid = request.args.get('StockId')
        stockid = str(stockid).upper()
        shares = request.args.get('Shares')
        tradedate = request.args.get('TradeDate')
        tradeprice = request.args.get('TradePrice')
        url = "http://comp9900fafafa.azurewebsites.net/api/Portfolio/DeleteTransaction?username="+username+"&portfolioname="+portfolioname+"&StockId="+stockid+"&Shares="+shares+"&TradeDate="+tradedate+"&TradePrice="+tradeprice
        response = urllib.urlopen(url)
        transactionStatus = json.loads(response.read())["Create Transaction Status"]
        if transactionStatus == "Success":
            return render_template('portfoliotransactioninfo.html', username=username, portfolio=portfolioname)
        else:
            return "Delete transaction Failed."

@app.route('/edittransaction', methods=['GET', 'POST'])
def edittransaction():
    username = session.get('username')
    if username is None:
        return render_template('home.html')
    else:
        if request.method == 'GET':
            portfolioname = request.args.get('Portfolioname')
            stockid = request.args.get('StockId')
            stockid = str(stockid).upper()
            shares = request.args.get('Shares')
            tradedate = request.args.get('TradeDate')
            tradeprice = request.args.get('TradePrice')
            return render_template('edittransaction.html', username=username, portfolio=portfolioname, stockid=stockid, shares=shares, tradedate=tradedate, tradeprice=tradeprice)
        else:
            portfolioname = request.args.get('Portfolioname')
            stockid = request.args.get('StockId')
            stockid = str(stockid).upper()
            shares = request.args.get('Shares')
            tradedate = request.args.get('TradeDate')
            tradeprice = request.args.get('TradePrice')
            newstockid = request.form.get('stockid')
            newstockid = str(newstockid).upper()
            newshares = request.form.get('shares')
            newtradedate = request.form.get('tradedate')
            newtradeprice = request.form.get('tradeprice')
            createurl = "http://comp9900fafafa.azurewebsites.net/api/Portfolio/CreateTransaction?username=" + username + "&portfolioname=" + portfolioname + "&StockId=" + newstockid + "&Shares=" + newshares + "&TradeDate=" + newtradedate + "&TradePrice=" + newtradeprice
            response = urllib.urlopen(createurl)
            createStatus = json.loads(response.read())["Create Transaction Status"]
            if createStatus == "Success":
                deleteurl = "http://comp9900fafafa.azurewebsites.net/api/Portfolio/DeleteTransaction?username=" + username + "&portfolioname=" + portfolioname + "&StockId=" + stockid + "&Shares=" + shares + "&TradeDate=" + tradedate + "&TradePrice=" + tradeprice
                response = urllib.urlopen(deleteurl)
                deleteStatus = json.loads(response.read())["Create Transaction Status"]
                if deleteStatus == "Success":
                    return render_template('portfoliotransactioninfo.html', username=username, portfolio=portfolioname)
            else:
                return "Edit failed"

@app.route('/news', methods=['GET'])
def shownews():
    stockid = request.args.get('stockid')
    stockid = str(stockid).upper()
    news_url = "http://comp9900fafafa.azurewebsites.net/api/BasicInfo/GetNews?stockId="
    news_response = urllib.urlopen(news_url + stockid)
    news = json.loads(news_response.read())
    username = session.get('username')
    relative = {}
    for news_ in news:
        if news_['relative'].split(',')[0] == 'N/A':
            relative[news_['title']] = []
            continue
        relative[news_['title']] = news_['relative'].split(',')

    if username is None:
        return render_template('news.html', stockid=stockid, news=news, relative=relative)
    else:
        return render_template('newslogin.html', stockid=stockid, news=news, username=username, relative=relative)

@app.route('/contact', methods=['GET'])
def showcontact():
    stockid = request.args.get('stockid')
    stockid = str(stockid).upper()
    url = "http://comp9900fafafa.azurewebsites.net/api/BasicInfo/GetBasicInfo?stockId="
    response = urllib.urlopen(url + stockid)
    stockInfos = json.loads(response.read())
    username = session.get('username')
    if username is None:
        return render_template('contact.html', stockid=stockid, result=stockInfos)
    else:
        return render_template('contactlogin.html', stockid=stockid, result=stockInfos, username=username)

@app.route('/usertransaction')
def usertransaction():
    username = session.get('username')
    if username is None:
        return render_template('home.html')
    else:
        return render_template('usertransaction.html', username=username)

@app.route('/usersummary')
def usersummary():
    username = session.get('username')
    if username is None:
        return render_template('home.html')
    else:
        return render_template('usersummary.html', username=username)

@app.route('/portfoliosummary')
def portfoliosummary():
    username = session.get('username')
    portfolioname = request.args.get('portfolioname')
    if username is None:
        return render_template('home.html')
    else:
        return render_template('portfoliosummaryinfo.html', username=username, portfolio=portfolioname)

@app.route('/userasset')
def userasset():
    username = session.get('username')
    if username is None:
        return render_template('home.html')
    else:
        return render_template('userasset.html', username=username)

@app.route('/portfolioasset')
def portfolioasset():
    username = session.get('username')
    portfolioname = request.args.get('portfolioname')
    if username is None:
        return render_template('home.html')
    else:
        return render_template('portfolioassetinfo.html', username=username, portfolio=portfolioname)

if __name__ == '__main__':
    app.run()
