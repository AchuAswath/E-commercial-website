from flask_wtf import FlaskForm

from market import db, bcrypt, login_manager, app
from market import Bcrypt
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return db.get_or_404(User, user_id)


class User(UserMixin,db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30))
    email_address = db.Column(db.String(100), unique=True)
    password_hash = db.Column(db.String(100), nullable=False)
    budget = db.Column(db.Integer, default=100000)

    items = db.relationship('Item', backref='owned_user', lazy=True)


class Item(UserMixin,db.Model):
    __tablename__ = 'item'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(length=50), nullable=False)
    barcode = db.Column(db.String(length=12), nullable=False)
    price = db.Column(db.Integer(), nullable=False)
    description = db.Column(db.String(length=1050), nullable=False, unique=True)
    owner_id = db.Column(db.Integer(), db.ForeignKey('user.id'))





with app.app_context():
    db.create_all()


    def __repr__(self):
        return f' {self.name}'
