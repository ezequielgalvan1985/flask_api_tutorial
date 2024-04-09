from flask import request, Blueprint
from flask_restful import Api, Resource
from schemas import RolSchema
from models import Rol
from db import db

rol_serializer = RolSchema()
roles_blueprint = Blueprint('rol_blueprint', __name__)
api = Api(roles_blueprint)


class RolListResource(Resource):
    def get(self):
        rols = db.session.execute(db.select(Rol).order_by(Rol.nombre)).scalars()
        result = rol_serializer.dump(rols, many=True)
        return result

    def post(self):
        data = request.get_json()
        record_dict = rol_serializer.load(data)
        rol = Rol(nombre=record_dict['nombre'],descripcion=record_dict['descripcion'])
        rol.save()
        resp = rol_serializer.dump(rol)
        return resp, 201


class RolResource(Resource):
    def get(self, id):
        r = Rol.get_by_id(id)
        if r is None:
            return {"mensaje": "rol no existe"}, 404
        resp = rol_serializer.dump(r)
        return resp

    def delete(self, id):
        r = Rol.get_by_id(id)
        if r is None:
            return {"mensaje": "rol no existe"}, 500
        rols = db.session.delete(r)
        db.session.commit()
        return '', 204

    def put(self, id):
        r = Rol.get_by_id(id)
        if r is None:
            return {"message": "No se encontro Id", "data": id}, 404

        data = request.get_json()
        record_dict = rol_serializer.load(data)
        r.nombre = record_dict['nombre']
        r.descripcion = record_dict['descripcion']
        r.save()
        resp = rol_serializer.dump(r)
        return {"message": "Actualizado Ok", "data": resp}, 200

api.add_resource(RolListResource, '/api/v1.0/roles',endpoint='rol_list_resource')
api.add_resource(RolResource, '/api/v1.0/roles/<int:id>', endpoint='rol_resource')
