from flask import request, Blueprint
from flask_restful import Api, Resource

from schemas import CategoriaSchema
from models import Categoria
from db import db

categoria_serializer = CategoriaSchema()
categorias_blueprint = Blueprint('categorias_blueprint', __name__)
api = Api(categorias_blueprint)


class CategoriaListResource(Resource):
    def get(self):
        print('flag1')
        categorias = db.session.execute(db.select(Categoria).order_by(Categoria.nombre)).scalars()
        result = categoria_serializer.dump(categorias, many=True)
        print('flag2')
        return result

    def post(self):
        data = request.get_json()
        record_dict = categoria_serializer.load(data)
        categoria = Categoria(nombre=record_dict['nombre'],
                              descripcion=record_dict['descripcion'])
        categoria.save()
        resp = categoria_serializer.dump(categoria)
        return resp, 201


class CategoriaResource(Resource):
    def get(self, id):
        r = Categoria.get_by_id(id)
        if r is None:
            return {"mensaje": "categoria no existe"}, 404
        resp = categoria_serializer.dump(r)
        return resp

    def delete(self, id):
        r = Categoria.get_by_id(id)
        if r is None:
            return {"mensaje": "categoria no existe"}, 500
        categorias = db.session.delete(r)
        db.session.commit()
        return '', 204

    def put(self, id):
        r = Categoria.get_by_id(id)
        if r is None:
            return {"message": "No se encontro Id", "data": id}, 404

        data = request.get_json()
        record_dict = categoria_serializer.load(data)
        r.nombre = record_dict['nombre']
        r.descripcion = record_dict['descripcion']
        r.save()
        resp = categoria_serializer.dump(r)
        return {"message": "Actualizado Ok", "data": resp}, 200

api.add_resource(CategoriaListResource, '/api/v1.0/categorias',endpoint='categorias_list_resource')
api.add_resource(CategoriaResource, '/api/v1.0/categorias/<int:id>', endpoint='categoria_resource')
