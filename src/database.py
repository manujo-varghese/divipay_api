
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key =True)
    username = db.Column(db.String(80),unique=True, nullable =False)
    email = db.Column(db.String(120),unique=True, nullable =False)
    password = db.Column(db.Text(), nullable =False)
    created = db.Column(db.DateTime,default=datetime.now())
    updated = db.Column(db.DateTime,onupdate=datetime.now())
    cards = db.relationship('Card',backref='user')

    def __repr__(self) -> str:
        return 'User>>> {self.username}'


class Card(db.Model):
    id = db.Column(db.String(80), primary_key =True)
    balance = db.Column(db.Integer, nullable = False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    created = db.Column(db.DateTime,default=datetime.now())
    updated = db.Column(db.DateTime,onupdate=datetime.now())
    card_controls = db.relationship('CardControl',backref='card')
    transactions = db.relationship('Transaction',backref='card')
    def __repr__(self) -> str:
        return 'Card>>> {self.id}'

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key =True)
    card_id = db.Column(db.String(80), db.ForeignKey('card.id'))
    amount = db.Column(db.Integer, nullable = False)
    merchant = db.Column(db.String(50), nullable = False)
    merchant_category = db.Column(db.Integer, nullable = True)
    created = db.Column(db.DateTime,default=datetime.now())
    updated = db.Column(db.DateTime,onupdate=datetime.now())

    def __repr__(self) -> str:
        return 'Transaction>>> {self.id}'

class CardControl(db.Model):
    id = db.Column(db.Integer, primary_key =True)
    card_id = db.Column(db.String(80), db.ForeignKey('card.id'))
    category_control = db.Column(db.Integer, nullable = True)
    merchant_control = db.Column(db.Integer, nullable = True)
    max_amount = db.Column(db.Integer, nullable = True)
    min_amount = db.Column(db.Integer, nullable = True)
    created = db.Column(db.DateTime,default=datetime.now())
    updated = db.Column(db.DateTime,onupdate=datetime.now())


    def __repr__(self) -> str:
        return 'CardControl>>> {self.id}'