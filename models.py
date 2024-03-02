from app import db
from werkzeug.security import generate_password_hash, check_password_hash

from datetime import date  # for use in class Product
from flask_sqlalchemy import SQLAlchemy


# We can use a different module to create our models. Let us use models.py. See the created file.

class User(db.Model):
    _tablename_ = 'userregister'
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(20), unique=False, nullable=False)
    lastname = db.Column(db.String(20), unique=False, nullable=False)
    othernames = db.Column(db.String(20), unique=False, nullable=True)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), unique=False, nullable=False)

    # represent the object when it is queried for
    def _repr_(self):
        return '<User {}>'.format(self.id)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)


class Product(db.Model):
    _tablename_ = 'product'
    orderid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=False, nullable=False)
    code = db.Column(db.String(20), unique=False, nullable=False)
    description = db.Column(db.Text, unique=False, nullable=True)
    price_per_unit = db.Column(db.Float, unique=False, nullable=False)
    product_inception_date = db.Column(db.Date, nullable=False,
                                       default=date.today())

    # represent the object when it is queried for
    def _repr_(self):
        return '<Product {}>'.format(self.id)


class Order(db.Model):
        _tablename_ = 'order'
        order_id = db.Column(db.Integer, primary_key=True)
        product_name = db.Column(db.String(25), unique=False, nullable=False)
        quantity = db.Column(db.Integer, unique=False, nullable=False)
        customer_id = db.Column(db.Integer, unique=True, nullable=True)


class Customer(db.Model):
    _tablename_ = 'customer'
    customer_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(25), unique=False, nullable=False)
    last_name = db.Column(db.String(20), unique=False, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), default='')