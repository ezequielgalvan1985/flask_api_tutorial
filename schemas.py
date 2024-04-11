from marshmallow import fields
from extensiones import ma

class UserSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    username = fields.String()
    email = fields.String()
    password = fields.String()
    rol_id = fields.Integer()
class UserSchemaDto(ma.Schema):
    id = fields.Integer(dump_only=True)
    username = fields.String()
    email = fields.String()

class PermisoSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    nombre = fields.String()
    descripcion = fields.String()
    recurso = fields.String()
    acceso = fields.String()

class CategoriaSchema(ma.Schema):
    id = fields.Integer(dump_only=False)
    nombre = fields.String()
    descripcion = fields.String()
    rubro_id = fields.Integer()

class MarcaSchema(ma.Schema):
    id = fields.Integer(dump_only=False)
    nombre = fields.String()
    descripcion = fields.String()


class RubroSchema(ma.Schema):
    id = fields.Integer(dump_only=False)
    nombre = fields.String()
    descripcion = fields.String()

class EmpresaSchema(ma.Schema):
    id = fields.Integer(dump_only=False)
    nombre = fields.String()
    descripcion = fields.String()
    frase = fields.String()
    direccion = fields.String()
    ciudad = fields.String()
    telefono = fields.String()
    rubro = ma.Nested(RubroSchema, many=False)
    rubro_id = fields.Integer()
    usuario = ma.Nested(UserSchema, many=False)
    usuario_id = fields.Integer()


class ProductoSchema(ma.Schema):
    id = fields.Integer(dump_only=False)
    nombre = fields.String()
    descripcion = fields.String()
    precio = fields.Float()
    categoria = ma.Nested(CategoriaSchema, many=False)
    marca = ma.Nested(MarcaSchema, many=False)
    empresa= ma.Nested(EmpresaSchema, many=False)
    precio_oferta = fields.Float()

class RolSchema(ma.Schema):
    id = fields.Integer(dump_only=False)
    nombre = fields.String()
    descripcion = fields.String()


class RolPermisoSchema(ma.Schema):
    id = fields.Integer(dump_only=False)
    rol_id = fields.Integer()
    permiso_id = fields.Integer()

