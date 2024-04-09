from flask import request, Blueprint
from flask_jwt_extended import jwt_required
from flask_restful import Api, Resource
from schemas import RolPermisoSchema
from models import Categoria, RolPermiso
from db import db

rolpermisos_serializer = RolPermisoSchema()
rolpermisos_blueprint = Blueprint('rolpermisos_blueprint', __name__)
api = Api(rolpermisos_blueprint)


class RolPermisoListResource(Resource):
    def get(self):
        rolpermisos = db.session.execute(db.select(RolPermiso).order_by(RolPermiso.rolId)).scalars()
        result = rolpermisos_serializer.dump(rolpermisos, many=True)
        return result

    def post(self):
        data = request.get_json()
        record_dict = rolpermisos_serializer.load(data)
        rolpermisos = RolPermiso(rolId=record_dict['rolId'],
                              permisoId=record_dict['permisoId'])
        rolpermisos.save()
        resp = rolpermisos_serializer.dump(rolpermisos)
        return resp, 201


class RolPermisoResource(Resource):
    def get(self, id):
        r = RolPermiso.get_by_id(id)
        if r is None:
            return {"mensaje": "rolpermisos no existe"}, 404
        resp = rolpermisos_serializer.dump(r)
        return resp

    def delete(self, id):
        r = RolPermiso.get_by_id(id)
        if r is None:
            return {"mensaje": "rolpermisos no existe"}, 500
        db.session.delete(r)
        db.session.commit()
        return '', 204

    def put(self, id):
        r = RolPermiso.get_by_id(id)
        if r is None:
            return {"message": "No se encontro Id", "data": id}, 404

        data = request.get_json()
        record_dict = rolpermisos_serializer.load(data)
        r.nombre = record_dict['nombre']
        r.descripcion = record_dict['descripcion']
        r.save()
        resp = rolpermisos_serializer.dump(r)
        return {"message": "Actualizado Ok", "data": resp}, 200

api.add_resource(RolPermisoListResource, '/api/v1.0/rolpermisos',endpoint='rolpermisos_list_resource')
api.add_resource(RolPermisoResource, '/api/v1.0/rolpermisos/<int:id>', endpoint='rolpermiso_resource')
