from routes.categories import category_api
from routes.clients import client_api
from routes.order_items import order_item_api
from routes.orders import order_api
from routes.products import product_api


def register_blueprints(app):
    app.register_blueprint(client_api)
    app.register_blueprint(product_api)
    app.register_blueprint(category_api)
    app.register_blueprint(order_api)
    app.register_blueprint(order_item_api)