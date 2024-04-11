from flask import request, Blueprint, abort
from flask_jwt_extended import jwt_required, get_jwt
from flask_restful import Api, Resource
from schemas import PublicidadSchema, RolPermisoSchema
from models import Publicidad, Permiso
from db import db
from flask_jwt_extended import get_jwt_identity
import json

publicidad_serializer = PublicidadSchema()
publicidades_blueprint = Blueprint('publicidades_blueprint', __name__)
api = Api(publicidades_blueprint)


class PublicidadListResource(Resource):
    @jwt_required()
    def get(self):
        claims = get_jwt()
        acceso = False
        publicidades = db.session.execute(db.select(Publicidad).order_by(Publicidad.titulo)).scalars()
        result = publicidad_serializer.dump(publicidades, many=True)
        return result

    def post(self):
        data = request.get_json()
        record_dict = publicidad_serializer.load(data)
        publicidad = Publicidad(titulo=record_dict['titulo'],
                                  descripcion=record_dict['descripcion'],
                                  empresa_id= record_dict['empresa']['id'],
                                  producto_id=record_dict['producto']['id']
                              )
        publicidad.precio = record_dict['precio']
        publicidad.descuento = record_dict['descuento']

        publicidad.save()
        resp = publicidad_serializer.dump(publicidad)
        return resp, 201


class PublicidadResource(Resource):
    def get(self, id):
        r = Publicidad.get_by_id(id)
        if r is None:
            return {"mensaje": "publicidad no existe"}, 404
        resp = publicidad_serializer.dump(r)
        return resp

    def delete(self, id):
        r = Publicidad.get_by_id(id)
        if r is None:
            return {"mensaje": "publicidad no existe"}, 500
        publicidades = db.session.delete(r)
        db.session.commit()
        return '', 204

    def put(self, id):
        r = Publicidad.get_by_id(id)
        if r is None:
            return {"message": "No se encontro Id", "data": id}, 404

        data = request.get_json()
        record_dict = publicidad_serializer.load(data)
        r.titulo = record_dict['titulo']
        r.descripcion = record_dict['descripcion']
        r.precio = record_dict['precio']
        r.descuento = record_dict['descuento']
        r.empresa_id = record_dict['empresa']['id'],
        r.producto_id = record_dict['producto']['id']
        r.save()
        resp = publicidad_serializer.dump(r)
        return {"message": "Actualizado Ok", "data": resp}, 200


api.add_resource(PublicidadListResource, '/api/v1.0/publicidades',endpoint='publicidades_list_resource')
api.add_resource(PublicidadResource, '/api/v1.0/publicidades/<int:id>', endpoint='publicidad_resource')
