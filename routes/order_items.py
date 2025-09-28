from flask import Blueprint, request, jsonify
from models import OrderItem, db
from schemas import OrderItemSchema
from marshmallow import ValidationError

order_item_api = Blueprint('order_item_api', __name__, url_prefix='/api/order_items')

order_item_schema = OrderItemSchema()
order_items_schema = OrderItemSchema(many=True)

@order_item_api.get('/')
def list_order_items():
    order_items = OrderItem.query.all()
    return jsonify(order_items_schema.dump(order_items)), 200

@order_item_api.post('/')
def create_order_item():
    request_data = request.get_json() or {}
    try:
        order_item = order_item_schema.load(request_data, session=db.session)
        db.session.add(order_item)
        db.session.commit()
        return jsonify(order_item_schema.dump(order_item)), 201
    except ValidationError as err:
        return jsonify({'errors': err.messages}), 400

@order_item_api.delete('/<int:item_id>')
def delete_order_item(item_id):
    order_item = OrderItem.query.get_or_404(item_id)
    db.session.delete(order_item)
    db.session.commit()
    return '', 204

@order_item_api.put('/<int:item_id>')
def update_order_item(item_id):
    order_item = OrderItem.query.get_or_404(item_id)
    data = request.get_json() or {}
    for key, value in data.items():
        if hasattr(order_item, key):
            setattr(order_item, key, value)
    db.session.commit()
    return jsonify(order_item_schema.dump(order_item)), 200
