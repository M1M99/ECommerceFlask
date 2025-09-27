from flask import Blueprint, jsonify, request
from models import db, Product, Category

api = Blueprint('api', __name__, url_prefix='/api')
#products
@api.route('/products', methods=['GET'])
def list_products():
    products = Product.query.all()
    return jsonify([{
        'id': p.id,
        'name': p.name,
        'price': p.price,
        'quantity': p.quantity,
        'category_id': p.category_id,
        'image_url':p.image_url,
        'category': {
            'id': p.category.id,
            'title': p.category.title,
            'description': p.category.description
        } if p.category else None
    } for p in products])

@api.route('/product', methods=['POST'])
def create_product():
    data = request.get_json()
    product = Product(name=data['name'], price=data['price'], category_id=data['category_id'], quantity=data['quantity'],image_url=data['image_url'])
    db.session.add(product)
    db.session.commit()
    return jsonify({'id': product.id, 'name': product.name}), 201

@api.route('product/category/<int:category_id>', methods=['GET'])
def get_product_by_category(category_id):
    category = Category.query.get(category_id)
    products = Product.query.filter_by(category_id=category_id).all()
    return jsonify([{'id':product.id,'name':product.name}for product in products])


@api.route('/product/<int:product_id>/delete', methods=['DELETE'])
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    return jsonify({'id': product.id}), 204


@api.route('/product/<int:product_id>', methods=['GET'])
def get_product(product_id):
    product = Product.query.get_or_404(product_id)
    return jsonify({
        'id': product.id,
        'name': product.name,
        'price': product.price,
        'quantity': product.quantity,
        'image_url':product.image_url,
        'category_id': product.category_id,
    })




@api.route('/product/<int:product_id>', methods=['PUT', 'PATCH'])
def update_product(product_id):
    product = Product.query.get_or_404(product_id)
    data = request.get_json(force=True, silent=True) or {}

    for key, value in data.items():
        if hasattr(product, key):
            setattr(product, key, value)

    db.session.commit()

    return jsonify({
        'id': product.id,
        'name': product.name,
        'price': product.price,
        'quantity': product.quantity,
        'category_id': product.category_id,
        'image_url':product.image_url,
    }), 200



#category endpoints
@api.route('/categories', methods=['GET'])
def list_categories():
    categories = Category.query.all()
    return jsonify([{
        'id':category.id,
        'title':category.title,
        'description':category.description,
    } for category in categories])

@api.route('/category', methods=['POST'])
def create_category():
    data =request.get_json()
    category = Category(title=data['title'], description=data['description'])
    db.session.add(category)
    db.session.commit()
    return jsonify({'id': category.id,'title':category.title}), 201

@api.route('/category/<int:category_id>/delete', methods=['DELETE'])
def delete_category(category_id):
    category = Category.query.get_or_404(category_id)
    db.session.delete(category)
    db.session.commit()
    return jsonify({'id': category.id }), 204


@api.route('/category/<int:category_id>', methods=['PUT', 'PATCH'])
def update_category(category_id):
    category = Category.query.get_or_404(category_id)
    data = request.get_json(force=True, silent=True) or {}

    for key, value in data.items():
        if hasattr(category, key):
            setattr(category, key, value)

    db.session.commit()

    return jsonify({
        'id': category.id,
        'title': category.title,
        'description': category.description
    }), 200


@api.route('/category/<int:category_id>', methods=['GET'])
def get_category(category_id):
    category = Category.query.get_or_404(category_id)
    return jsonify({'id': category.id,'title':category.title,'description':category.description}), 200