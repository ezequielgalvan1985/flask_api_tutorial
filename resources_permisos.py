from flask import request, Blueprint
from flask_jwt_extended import jwt_required
from flask_restful import Api, Resource
from schemas import PermisoSchema
from models import Permiso
from db import db

permiso_serializer = PermisoSchema()
permisos_blueprint = Blueprint('permisos_blueprint', __name__)
api = Api(permisos_blueprint)


class PermisoListResource(Resource):
    @jwt_required()
    def get(self):
        permisos = db.session.execute(db.select(Permiso).order_by(Permiso.nombre)).scalars()
        result = permiso_serializer.dump(permisos, many=True)
        print('flag2')
        return result

    def post(self):
        data = request.get_json()
        record_dict = permiso_serializer.load(data)
        permiso = Permiso()
        permiso.nombre = record_dict['nombre']
        permiso.descripcion=record_dict['descripcion']
        permiso.recurso= record_dict['recurso']
        permiso.acceso = record_dict['acceso']
        permiso.save()
        resp = permiso_serializer.dump(permiso)
        return resp, 201


class PermisoResource(Resource):
    def get(self, id):
        r = Permiso.get_by_id(id)
        if r is None:
            return {"mensaje": "permiso no existe"}, 404
        resp = permiso_serializer.dump(r)
        return resp

    def delete(self, id):
        r = Permiso.get_by_id(id)
        if r is None:
            return {"mensaje": "permiso no existe"}, 500
        permisos = db.session.delete(r)
        db.session.commit()
        return '', 204

    def put(self, id):
        r = Permiso.get_by_id(id)
        if r is None:
            return {"message": "No se encontro Id", "data": id}, 404

        data = request.get_json()
        record_dict = permiso_serializer.load(data)
        r.nombre = record_dict['nombre']
        r.descripcion = record_dict['descripcion']
        r.save()
        resp = permiso_serializer.dump(r)
        return {"message": "Actualizado Ok", "data": resp}, 200

api.add_resource(PermisoListResource, '/api/v1.0/permisos',endpoint='permisos_list_resource')
api.add_resource(PermisoResource, '/api/v1.0/permisos/<int:id>', endpoint='permiso_resource')