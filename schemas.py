from marshmallow import fields
from extensiones import ma

class UserSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    username = fields.String()
    email = fields.String()
    password = fields.String()
    rol_id = fields.Integer()
class UserSchemaDto(ma.Schema):
    id = fields.Integer(dump_only=False)
    username = fields.String()


class DatoPersonalSchema(ma.Schema):
    id = fields.Integer(dump_only=False)
    nombre = fields.String()
    apellido = fields.String()
    direccion = fields.String()
    ciudad = fields.String()
    telefono = fields.String()
    user = ma.Nested(UserSchemaDto, many=False)


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

class RubroSchemaDto(ma.Schema):
    id = fields.Integer(dump_only=False)
    nombre = fields.String()

class EmpresaSchema(ma.Schema):
    id = fields.Integer(dump_only=False)
    nombre = fields.String()
    descripcion = fields.String()
    frase = fields.String()
    direccion = fields.String()
    ciudad = fields.String()
    telefono = fields.String()
    rubro = ma.Nested(RubroSchema, many=False)
    usuario = ma.Nested(UserSchemaDto, many=False)


class EmpresaSchemaDto(ma.Schema):
    id = fields.Integer(dump_only=False)
    nombre = fields.String()
    rubro = ma.Nested(RubroSchemaDto, many=False)
    usuario = ma.Nested(UserSchemaDto, many=False)


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

class PublicidadSchema(ma.Schema):
    id = fields.Integer(dump_only=False)
    titulo = fields.String()
    descripcion = fields.String()
    cantidad =fields.Float()
    precio = fields.Float()
    descuento = fields.Float()
    empresa = ma.Nested(EmpresaSchema, many=False)
    producto= ma.Nested(ProductoSchema, many=False)


class PedidoitemSchema(ma.Schema):
    id = fields.Integer(dump_only=False)
    cantidad = fields.Integer()
    producto = ma.Nested(ProductoSchema, many=False)
    pedido = fields.Integer()



class PedidoSchema(ma.Schema):
    id = fields.Integer(dump_only=False)
    fecha = fields.String()
    estado = fields.String()
    importeenvio = fields.Float()
    direccion = fields.String()
    empresa = ma.Nested(EmpresaSchema, many=False)
    user = ma.Nested(UserSchema, many=False)
    items = ma.Nested(PedidoitemSchema, many=True)

class PedidoFindByUserEmpresaRequestSchemaDto(ma.Schema):
    user_id = fields.Integer()
    empresa_id= fields.Integer()

class PedidoItemSchemaDto(ma.Schema):
    id = fields.Integer(dump_only=False)
    pedido_id = fields.Integer()
    producto_id = fields.Integer()
    cantidad = fields.Float()

class PedidoDtoSchema(ma.Schema):
    id = fields.Integer(dump_only=False)
    fecha = fields.String()
    estado = fields.String()
    importeenvio = fields.Float()
    direccion = fields.String()
    empresa = ma.Nested(EmpresaSchemaDto, many=False)
    user = ma.Nested(UserSchemaDto, many=False)
    items = ma.Nested(PedidoitemSchema, many=True)
