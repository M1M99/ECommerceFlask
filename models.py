from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(70),nullable=False)
    price = db.Column(db.Float,default=1)
    quantity = db.Column(db.Integer,default=1)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    image_url = db.Column(db.String(70),nullable=True)
    category = db.relationship('Category', back_populates='products')


class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(20),nullable=False)
    description = db.Column(db.String(70),nullable=True)
    products = db.relationship('Product', back_populates='category')


class Client(db.Model):
    __tablename__ = 'clients'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(25),nullable=False)
    surname = db.Column(db.String,nullable=True)
    email = db.Column(db.String)
    phone = db.Column(db.String)
    address = db.Column(db.String)
    orders = db.relationship('Order', back_populates='client')


class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'))
    client = db.relationship('Client', back_populates='orders')

    items = db.relationship('OrderItem', back_populates='order', cascade='all, delete-orphan')

class OrderItem(db.Model):
    __tablename__ = 'order_items'
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'))
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'))
    quantity = db.Column(db.Integer, nullable=False, default=1)

    order = db.relationship('Order', back_populates='items')
    product = db.relationship('Product')
