from app import app
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash,check_password_hash

#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'

db=SQLAlchemy(app)

class User(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String[32],unique=True)
    passhash=db.Column(db.String[256],nullable=False)
    name=db.Column(db.String[64],nullable=False)
    is_admin=db.Column(db.Boolean,nullable=False,default=False)
    
class Category(db.Model):
     id=db.Column(db.Integer,primary_key=True)
     name=db.Column(db.String[64],nullable=False)
     
     products=db.relationship('Product',backref='category',lazy=True)
     
class Product(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String[64],nullable=False)
    price=db.Column(db.Float,nullable=False)
    category_id=db.Column(db.Integer,db.ForeignKey('category.id'),nullable=False)
    quantity=db.Column(db.Integer,nullable=False)
    man_date=db.Column(db.Date,nullable=False)
    
    carts=db.relationship('Cart',backref='product',lazy=True)
    orders=db.relationship('Order',backref='product',lazy=True)
    
class Cart(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    user_id=db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)
    product_id=db.Column(db.Integer,db.ForeignKey('product.id'),nullable=False)
    quantity=db.Column(db.Integer,nullable=False)
    
class Transaction(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    user_id=db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)
    datetime=db.Column(db.DateTime,nullable=False)
    
    orders=db.relationship('Order',backref='transaction',lazy=True)
    
class Order(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    transaction_id=db.Column(db.Integer,db.ForeignKey('transaction.id'),nullable=False)
    product_id=db.Column(db.Integer,db.ForeignKey('product.id'),nullable=False)
    quantity=db.Column(db.Integer,nullable=False)
    price=db.Column(db.Float,nullable=False)
    
with app.app_context():
    db.create_all()
    
    #checking for admin 
    #we will create one admin from our side in the backend
    admin=User.query.filter_by(is_admin=True).first()
    if not admin:
        password_hash=generate_password_hash('admin')
        admin=User(username='admin',passhash=password_hash,name='Admin',is_admin=True)
        db.session.add(admin)
        db.session.commit()

    
    
    