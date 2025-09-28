from marshmallow import fields
from marshmallow_sqlalchemy import SQLAlchemySchema, SQLAlchemyAutoSchema

from models import Category, Product, Client


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
