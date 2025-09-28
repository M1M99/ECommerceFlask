from flask import Blueprint, jsonify, request

from models import Category, db
from schemas import CategorySchema
category_schema = CategorySchema()
category_list_schema = CategorySchema(many=True)
category_api = Blueprint('category_api', __name__, url_prefix='/api')


@category_api.route('/categories', methods=['GET'])
def list_categories():
    categories = Category.query.all()
    return jsonify(category_list_schema.dump(categories))

@category_api.route('/category', methods=['POST'])
def create_category():
    data =request.get_json()
    category = Category(title=data['title'], description=data['description'])
    db.session.add(category)
    db.session.commit()
    return jsonify(category_schema.dump(category)), 201

@category_api.route('/category/<int:category_id>/delete', methods=['DELETE'])
def delete_category(category_id):
    category = Category.query.get_or_404(category_id)
    db.session.delete(category)
    db.session.commit()
    return jsonify({'id': category.id }), 204


@category_api.route('/category/<int:category_id>', methods=['PUT', 'PATCH'])
def update_category(category_id):
    category = Category.query.get_or_404(category_id)
    data = request.get_json(force=True, silent=True) or {}

    for key, value in data.items():
        if hasattr(category, key):
            setattr(category, key, value)

    db.session.commit()
    return category_schema.dump(category), 200

@category_api.route('/category/<int:category_id>', methods=['GET'])
def get_category(category_id):
    category = Category.query.get_or_404(category_id)
    return jsonify(category_schema.dump(category)), 200