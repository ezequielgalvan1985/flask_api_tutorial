from flask import request, Blueprint
#from flask_jwt import jwt_required
from flask_restful import Api, Resource

from schemas import RubroSchema
from models import Rubro
from db import db

rubro_serializer = RubroSchema()
rubros_blueprint = Blueprint('rubros_blueprint', __name__)
api = Api(rubros_blueprint)


class RubroListResource(Resource):
    def get(self):
        rubros = db.session.execute(db.select(Rubro).order_by(Rubro.nombre)).scalars()
        result = rubro_serializer.dump(rubros, many=True)
        return result

    def post(self):
        data = request.get_json()
        record_dict = rubro_serializer.load(data)
        r = Rubro(nombre=record_dict['nombre'],descripcion=record_dict['descripcion'])
        r.icon = record_dict['icon']
        r.clase = record_dict['clase']

        r.save()
        resp = rubro_serializer.dump(r)
        return resp, 201


class RubroResource(Resource):
    def get(self, id):
        r = Rubro.get_by_id(id)
        if r is None:
            return {"mensaje": "rubro no existe"}, 404
        resp = rubro_serializer.dump(r)
        return resp

    def delete(self, id):
        r = Rubro.get_by_id(id)
        if r is None:
            return {"mensaje": "rubro no existe"}, 500
        rubros = db.session.delete(r)
        db.session.commit()
        return '', 204

    def put(self, id):
        r = Rubro.get_by_id(id)
        if r is None:
            return {"message": "No se encontro Id", "data": id}, 404

        data = request.get_json()
        record_dict = rubro_serializer.load(data)
        r.nombre = record_dict['nombre']
        r.descripcion = record_dict['descripcion']
        r.icon = record_dict['icon']
        r.clase = record_dict['clase']

        r.save()
        resp = rubro_serializer.dump(r)
        return {"message": "Actualizado Ok", "data": resp}, 200

api.add_resource(RubroListResource, '/api/v1.0/rubros',endpoint='rubros_list_resource')
api.add_resource(RubroResource, '/api/v1.0/rubros/<int:id>', endpoint='rubro_resource')
