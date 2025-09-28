from flask import Blueprint, jsonify, request
from models import db, Product, Category
from schemas import ProductSchema, CategorySchema

product_api = Blueprint('api', __name__, url_prefix='/api')
product_schema = ProductSchema()
product_list_schema = ProductSchema(many=True)
#products

@product_api.route('/products', methods=['GET'])
def list_products():
    products = Product.query.all()
    return jsonify(product_list_schema.dump(products))

@product_api.route('/product', methods=['POST'])
def create_product():
    data = request.get_json()
    product = Product(name=data['name'], price=data['price'], category_id=data['category_id'], quantity=data['quantity'],image_url=data['image_url'])
    db.session.add(product)
    db.session.commit()
    return jsonify(product_schema.dump(product)), 201

@product_api.route('product/category/<int:category_id>', methods=['GET'])
def get_product_by_category(category_id):
    category = Category.query.get(category_id)
    products = Product.query.filter_by(category_id=category_id).all()
    return jsonify(product_list_schema.dump(products))


@product_api.route('/product/<int:product_id>/delete', methods=['DELETE'])
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    return jsonify({'id': product.id}), 204


@product_api.route('/product/<int:product_id>', methods=['GET'])
def get_product(product_id):
    product = Product.query.get_or_404(product_id)
    return jsonify(product_schema.dump(product))

@product_api.route('/product/<int:product_id>', methods=['PUT', 'PATCH'])
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




