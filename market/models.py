from market import db
from market import login
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import UserMixin

@login.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(UserMixin, db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(length=30), nullable=False, unique=True)
    email_address = db.Column(db.String(length=50), nullable=False, unique=True)
    password_hash = db.Column(db.String(length=60), nullable=False)
    budget = db.Column(db.Integer(), nullable=False, default=1000)
    items = db.relationship('Item', backref='owned_user', lazy=True)

    def __repr__(self):
        return f'{self.username}'
    @property
    def budget_prettier(self):
        if len(str(str(self.budget))) >= 4:
            return f"{str(self.budget)[:-3]},{str(self.budget)[-3:]}"
        else:
            return f"{str(self.budget)}"
    def set_password(self,plain_text_password):
        self.password_hash = generate_password_hash(plain_text_password)
    def check_password(self,attempted_password):
        return check_password_hash(self.password_hash, attempted_password)
    def can_purchase(self, item_object):
        return self.budget >= item_object.price
class Item(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(length=50), nullable=False, unique=True)
    barcode = db.Column(db.String(length=20), nullable=False, unique=True)
    price = db.Column(db.Integer(), nullable=False)
    description = db.Column(db.String(length=1024), nullable=False, unique=True)
    owner = db.Column(db.Integer(), db.ForeignKey('user.id'))


    def __repr__(self):
        return f"{self.name}"

    def buy(self, current_user):
        self.owner = current_user.id
        current_user.budget -= self.price

    def sell(self,current_user):
        self.owner = None
        current_user.budget += self.price

