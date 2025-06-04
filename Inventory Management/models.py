from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()

class User(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100),unique=True, nullable = False)
    password = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(50), default='staff')
    created_at = db.Column(db.DateTime(datetime.utcnow))

class Category(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(100),nullable=False)
    created_at = db.Column(db.DateTime(datetime.utcnow))

class Supplier(db.Model):
    id = db.Column(db.Integer, primary_key =True)
    name = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime(datetime.utcnow))

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Integer, default = 0)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    supplier_id = db.Column(db.Integer, db.ForeignKey('supplier.id'))
    created_at = db.Column(db.DateTime(datetime.utcnow))

    category = db.relationship('Category')
    supplier = db.relationship('Supplier')

