from flask import Flask, render_template, request, url_for, redirect
import config
from exts import db
from models import User

app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)

# Create all tables;
# with app.app_context():
#     db.create_all()

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
        username = request.form.get('username')
        password = request.form.get('password')
        password_check = User.query.filter(User.username == username).first()
        if password == password_check:
            return redirect(url_for('dashboard'))
        else:
            return 'Wrong password'

@app.route('/register/', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    else:
        username = request.form.get('username')
        email = request.form.get('email')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter(User.email == email).first()
        if user:
            return 'User existed'
        else:
            if password1 != password2:
                return 'Password confirmation error'
            else:
                user = User(username=username, email=email, password=password1)
                db.session.add(user)
                db.session.commit()
                return redirect(url_for('login'))

if __name__ == '__main__':
    app.run()
