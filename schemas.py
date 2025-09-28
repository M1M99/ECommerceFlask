from marshmallow import fields
from marshmallow_sqlalchemy import SQLAlchemySchema, SQLAlchemyAutoSchema

from models import Category, Product, Client, Order, OrderItem


class CategorySchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Category
        load_instance = True

class ProductSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Product
        include_fk = True
        load_instance = True
    category = fields.Nested(CategorySchema,dump_only=True)

class ClientSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Client
        include_fk = True
        load_instance = True

class OrderItemSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = OrderItem
        include_fk = True
        load_instance = True

class OrderSchema(SQLAlchemyAutoSchema):
    items = fields.Nested(OrderItemSchema, many=True)

    class Meta:
        model = Order
        include_fk = True
        load_instance = True
