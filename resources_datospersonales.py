from flask import request, Blueprint, abort
from flask_jwt_extended import jwt_required, get_jwt
from flask_restful import Api, Resource
from schemas import DatoPersonalSchema, RolPermisoSchema
from models import Datopersonal, Permiso, User
from db import db
from flask_jwt_extended import get_jwt_identity
import json

datopersonal_serializer = DatoPersonalSchema()
datospersonales_blueprint = Blueprint('datospersonales_blueprint', __name__)
api = Api(datospersonales_blueprint)


class DatopersonalListResource(Resource):
    @jwt_required()
    def get(self):
        claims = get_jwt()
        acceso = False
        datopersonals = db.session.execute(db.select(Datopersonal).order_by(Datopersonal.nombre)).scalars()
        result = datopersonal_serializer.dump(datopersonals, many=True)
        return result

    def post(self):
        data = request.get_json()
        record_dict = datopersonal_serializer.load(data)
        datopersonal = Datopersonal(record_dict['nombre'])
        datopersonal.user = User.get_by_id(record_dict['user']['id'])
        if datopersonal.user is None:
            return {"mensaje": "Usuario no existe"}, 500

        datopersonal.apellido = record_dict['apellido']
        datopersonal.direccion = record_dict['direccion']
        datopersonal.ciudad = record_dict['ciudad']

        datopersonal.save()
        resp = datopersonal_serializer.dump(datopersonal)
        return resp, 201


class DatopersonalResource(Resource):
    def get(self, id):
        r = Datopersonal.get_by_id(id)
        if r is None:
            return {"mensaje": "datopersonal no existe"}, 404
        resp = datopersonal_serializer.dump(r)
        return resp

    def delete(self, id):
        r = Datopersonal.get_by_id(id)
        if r is None:
            return {"mensaje": "datopersonal no existe"}, 500
        datopersonals = db.session.delete(r)
        db.session.commit()
        return '', 204

    def put(self, id):
        r = Datopersonal.get_by_id(id)
        if r is None:
            return {"message": "No se encontro Id", "data": id}, 404

        data = request.get_json()
        record_dict = datopersonal_serializer.load(data)
        r.nombre = record_dict['nombre']
        r.user = User.get_by_id(record_dict['user']['id'])
        if r.user is None:
            return {"mensaje": "Usuario no existe"}, 500

        r.apellido = record_dict['apellido']
        r.direccion = record_dict['direccion']
        r.ciudad = record_dict['ciudad']
        r.nombre = record_dict['nombre']
        r.telefono = record_dict['telefono']
        r.save()
        resp = datopersonal_serializer.dump(r)
        return {"message": "Actualizado Ok", "data": resp}, 200


api.add_resource(DatopersonalListResource, '/api/v1.0/datospersonales',endpoint='datopersonals_list_resource')
api.add_resource(DatopersonalResource, '/api/v1.0/datospersonales/<int:id>', endpoint='datopersonal_resource')
