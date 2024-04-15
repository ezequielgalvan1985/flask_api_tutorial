from flask import request, Blueprint, abort
from flask_jwt_extended import jwt_required, get_jwt
from flask_restful import Api, Resource
from schemas import CategoriaSchema, RolPermisoSchema
from models import Categoria, Permiso
from db import db
from flask_jwt_extended import get_jwt_identity
import json

categoria_serializer = CategoriaSchema()
categorias_blueprint = Blueprint('categorias_blueprint', __name__)
api = Api(categorias_blueprint)


class CategoriaListResource(Resource):
    @jwt_required()
    def get(self):
        claims = get_jwt()
        acceso = False
        '''
        permisoRequerido= Permiso.query.filter_by(recurso='categorias').first()
        if permisoRequerido is None:
            return abort(500, "NO Existe Permiso Categoria")

        for item in claims['permisos']:
            if item["permisoId"] == permisoRequerido.id:
                acceso = True

        if acceso is False:
            return abort(403, "Usuario no esta Autorizado")
        '''
        categorias = db.session.execute(db.select(Categoria).order_by(Categoria.nombre)).scalars()
        result = categoria_serializer.dump(categorias, many=True)
        return result

    def post(self):
        data = request.get_json()
        record_dict = categoria_serializer.load(data)
        categoria = Categoria(nombre=record_dict['nombre'],
                              descripcion=record_dict['descripcion'])
        categoria.rubro_id = record_dict['rubro_id']

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
        r.rubroId = record_dict['rubro_id']
        r.save()
        resp = categoria_serializer.dump(r)
        return {"message": "Actualizado Ok", "data": resp}, 200


api.add_resource(CategoriaListResource, '/api/v1.0/categorias',endpoint='categorias_list_resource')
api.add_resource(CategoriaResource, '/api/v1.0/categorias/<int:id>', endpoint='categoria_resource')

#Metodos personalizados

categorias_findbyrubro_blueprint = Blueprint('categorias_findbyrubro_bp', __name__)
@categorias_findbyrubro_blueprint.route("/api/v1.0/categorias/consultas/findbyrubro/<int:rubro_id>", methods=["GET"])
@jwt_required()
def categoriasFindByRubro(rubro_id):
    c=Categoria.query.filter_by(rubro_id=rubro_id).all()
    if c is None:
        return abort(500, "No existen Categorias para el Rubro "+ rubro_id)
    resp = categoria_serializer.dump(c,many=True)
    return resp,200