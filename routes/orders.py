from flask import Blueprint, request, jsonify
from marshmallow import ValidationError

from models import Order, db
from schemas import OrderSchema

order_api = Blueprint('order_api', __name__, url_prefix='/api/orders')

order_list_schema = OrderSchema(many=True)
order_schema = OrderSchema()
@order_api.get('/')
def list_orders():
    orders = Order.query.all()
    return jsonify(order_list_schema.dump(orders))

@order_api.post('/create')
def create_order():
    request_data = request.get_json() or {}
    try:
        order = order_schema.load(request_data,session=db.session)
        db.session.add(order)
        db.session.commit()
        return jsonify(order_schema.dump(order)), 201
    except ValidationError as e:
        return jsonify({'message': e.messages}),400



@order_api.get('/client/<int:client_id>')
def list_orders_by_client(client_id):
    orders = Order.query.filter_by(client_id=client_id).all()
    return jsonify(order_list_schema.dump(orders)),200
