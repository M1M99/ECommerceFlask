from flask import Blueprint, jsonify, request, abort
from models import db, Product
from schemas import ProductSchema

product_api = Blueprint('product_api', __name__, url_prefix='/api/products')

product_schema = ProductSchema()
product_list_schema = ProductSchema(many=True)


@product_api.route('/', methods=['GET'])
def list_products():
    products = Product.query.all()
    return jsonify(product_list_schema.dump(products)), 200


@product_api.route('/', methods=['POST'])
def create_product():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No input data provided'}), 400

    product = Product(
        name=data.get('name'),
        price=data.get('price'),
        category_id=data.get('category_id'),
        quantity=data.get('quantity'),
        image_url=data.get('image_url')
    )

    db.session.add(product)
    db.session.commit()

    return jsonify(product_schema.dump(product)), 201


@product_api.route('/category/<int:category_id>', methods=['GET'])
def get_products_by_category(category_id):
    products = Product.query.filter_by(category_id=category_id).all()
    return jsonify(product_list_schema.dump(products)), 200


@product_api.route('/<int:product_id>', methods=['GET'])
def get_product(product_id):
    product = Product.query.get_or_404(product_id)
    return jsonify(product_schema.dump(product)), 200


@product_api.route('/<int:product_id>', methods=['PUT', 'PATCH'])
def update_product(product_id):
    product = Product.query.get_or_404(product_id)
    data = request.get_json() or {}

    for key, value in data.items():
        if hasattr(product, key):
            setattr(product, key, value)

    db.session.commit()

    return jsonify(product_schema.dump(product)), 200


@product_api.route('/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    return '', 204
