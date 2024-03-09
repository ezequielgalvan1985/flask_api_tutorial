from marshmallow import fields
from extensiones import ma

class UserSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    username = fields.String()
    email = fields.String()


class CategoriaSchema(ma.Schema):
    id = fields.Integer(dump_only=False)
    nombre = fields.String()
    descripcion = fields.String()


class ProductoSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    nombre = fields.String()
    descripcion = fields.String()
    precio = fields.Float()
    categoria = ma.Nested(CategoriaSchema, many=False)
