from flask import request, Blueprint
from flask_restful import Api, Resource, abort
from schemas import ProductoSchema
from models import Producto, Categoria
from db import db
producto_serializer = ProductoSchema()
productos_blueprint = Blueprint('productos_blueprint', __name__)
api = Api(productos_blueprint)


class ProductoListResource(Resource):
    def get(self):
        productos = db.session.execute(db.select(Producto).order_by(Producto.nombre)).scalars()
        result = producto_serializer.dump(productos, many=True)
        return result

    def post(self):
        data = request.get_json()
        record_dict = producto_serializer.load(data)
        producto = Producto(nombre=record_dict['nombre'],
                            descripcion=record_dict['descripcion'],
                            precio = record_dict['precio'])
        producto.categoria = Categoria.get_by_id(record_dict['categoria']['id'])
        if producto.categoria is None:
            abort(404, description="No se encontro Categoria")
        producto.save()
        resp = producto_serializer.dump(producto)
        return resp, 201


class ProductoResource(Resource):
    def get(self, id):
        r = Producto.get_by_id(id)
        if r is None:
            abort(404, description="No se encontro Producto")
        resp = producto_serializer.dump(r)
        return resp

    def delete(self, id):
        r = Producto.get_by_id(id)
        if r is None:
            abort(404, description="No se encontro Producto")
        productos = db.session.delete(r)
        db.session.commit()
        return '', 204

    def put(self, id):
        r = Producto.get_by_id(id)
        if r is None:
            abort(404, description="No se encontro Producto")
        data = request.get_json()
        record_dict = producto_serializer.load(data)
        r.nombre = record_dict['nombre']
        r.descripcion = record_dict['descripcion']
        r.precio = record_dict['precio']
        r.categoria = Categoria.get_by_id(record_dict['categoria']['id'])
        if r.categoria is None:
            abort(404, description="No se encontro Categoria")

        r.save()
        resp = producto_serializer.dump(r)
        return {"message": "Actualizado Ok", "data": resp}, 200

api.add_resource(ProductoListResource, '/api/v1.0/productos',endpoint='productos_list_resource')
api.add_resource(ProductoResource, '/api/v1.0/productos/<int:id>', endpoint='producto_resource')
