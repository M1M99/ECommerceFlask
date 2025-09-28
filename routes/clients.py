from flask import Blueprint, jsonify, request
from models import Client, db
from schemas import ClientSchema

client_api = Blueprint('client_api', __name__, url_prefix='/api/clients')
client_schema = ClientSchema()
client_list_schema = ClientSchema(many=True)

@client_api.get('/')
def list_clients():
    clients = Client.query.all()
    return jsonify(client_list_schema.dump(clients))

@client_api.post('/')
def create_client():
    request_data = request.get_json()
    client = client_schema.load(request_data, session=db.session)
    db.session.add(client)
    db.session.commit()
    return jsonify(client_schema.dump(client)), 201

@client_api.delete('/<int:client_id>')
def delete_client(client_id):
    client = Client.query.get_or_404(client_id)
    db.session.delete(client)
    db.session.commit()
    return jsonify(client_schema.dump(client)), 204

@client_api.put('/<int:client_id>')
def update_client(client_id):
    client = Client.query.get_or_404(client_id)
    request_data = request.get_json() or {}
    for key, value in request_data.items():
        if hasattr(client, key):
            setattr(client, key, value)
    db.session.commit()
    return jsonify(client_schema.dump(client)), 200

