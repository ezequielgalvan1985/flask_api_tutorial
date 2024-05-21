from flask import request, Blueprint, abort
from flask_cors import cross_origin
from flask_restful import Api, Resource
from schemas import ProductoSchema
from models import Producto, Categoria, Empresa, Marca
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
        print("aqui_entro")
        data = request.get_json()
        print("aqui_entro2")
        print(data)
        record_dict = producto_serializer.load(data)
        print("aqui_entro3")

        producto = Producto(nombre=record_dict['nombre'],
                            descripcion=record_dict['descripcion'],
                            precio = record_dict['precio'])
        producto.categoria = Categoria.get_by_id(record_dict['categoria']['id'])
        if not record_dict['empresa']['id'] is None:
            if producto.empresa is None:
                abort(404, "No se encontro Empresa")
            producto.empresa = Empresa.get_by_id(record_dict['empresa']['id'])
        producto.marca = Marca.get_by_id(record_dict['marca']['id'])
        producto.precio_oferta=record_dict['precio_oferta']
        if producto.categoria is None:
            abort(404, "No se encontro Categoria")
        producto.save()
        resp = producto_serializer.dump(producto)
        print("aqui_entro3")
        return resp, 201


class ProductoResource(Resource):
    def get(self, id):
        r = Producto.get_by_id(id)

        if r is None:
            abort(404, "No se encontro Producto")
        resp = producto_serializer.dump(r)
        return resp

    def delete(self, id):
        r = Producto.get_by_id(id)
        if r is None:
            abort(404, "No se encontro Producto")
        productos = db.session.delete(r)
        db.session.commit()
        return '', 204

    def put(self, id):
        r = Producto.get_by_id(id)
        if r is None:
            abort(404, "No se encontro Producto")
        data = request.get_json()
        record_dict = producto_serializer.load(data)
        r.nombre = record_dict['nombre']
        r.descripcion = record_dict['descripcion']
        r.precio = record_dict['precio']
        r.precio_oferta = record_dict['precio_oferta']

        r.categoria = Categoria.get_by_id(record_dict['categoria']['id'])
        if r.categoria is None:
            abort(404, "No se encontro Categoria")

        r.marca = Marca.get_by_id(record_dict['marca']['id'])
        if r.marca is None:
            abort(404, "No se encontro Marca")

        if not record_dict['empresa']['id'] is None:
            if r.empresa is None:
                abort(404, "No se encontro Empresa")
            r.empresa = Marca.get_by_id(record_dict['marca']['id'])
        r.save()
        resp = producto_serializer.dump(r)
        return {"message": "Actualizado Ok", "data": resp}, 200

api.add_resource(ProductoListResource, '/api/v1.0/productos',endpoint='productos_list_resource')
api.add_resource(ProductoResource, '/api/v1.0/productos/<int:id>', endpoint='producto_resource')
