from exts import db

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(50), nullable=False)
    # Implement the Email validation API later
    email = db.Column(db.String(50), nullable=False)

class Portfolio(db.Model):
    __tablename__ = 'portfolio'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    owner = db.relationship('User', backref=db.backref('portfolios'))

class Stock(db.Model):
    __tablename__ = 'stock'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ticker_symbol = db.Column(db.String(10), nullable=False)
    company = db.Column(db.String(50), nullable=False)
    main_properties = db.Column(db.String(50))

class Possession(db.Model):
    __tablename__ = 'possession'
    portfolio_id = db.Column(db.Integer, db.ForeignKey('portfolio.id'), primary_key=True)
    stock_id = db.Column(db.Integer, db.ForeignKey('stock.id'), primary_key=True)
    portfolio = db.relationship('Portfolio', backref=db.backref('possession'))
    stock = db.relationship('Stock', backref=db.backref('possession'))
    purchase_time = db.Column(db.Time, nullable=False)
    purchase_amount = db.Column(db.Integer, nullable=False)
    purchase_price = db.Column(db.Numeric, nullable=False)
