from flask import request, Blueprint, abort
from flask_jwt_extended import jwt_required, get_jwt
from flask_restful import Api, Resource
from schemas import EmpresaSchema, RolPermisoSchema
from models import Empresa, Permiso, Rubro, User
from db import db
from flask_jwt_extended import get_jwt_identity
import json

empresa_serializer = EmpresaSchema()
empresas_blueprint = Blueprint('empresas_blueprint', __name__)
api = Api(empresas_blueprint)


class EmpresaListResource(Resource):
    @jwt_required()
    def get(self):
        claims = get_jwt()
        acceso = False
        '''
        permisoRequerido= Permiso.query.filter_by(recurso='empresas').first()
        if permisoRequerido is None:
            return abort(500, "NO Existe Permiso Empresa")

        for item in claims['permisos']:
            if item["permisoId"] == permisoRequerido.id:
                acceso = True

        if acceso is False:
            return abort(403, "Usuario no esta Autorizado")
        '''
        empresas = db.session.execute(db.select(Empresa).order_by(Empresa.nombre)).scalars()
        result = empresa_serializer.dump(empresas, many=True)
        return result

    def post(self):
        data = request.get_json()
        record_dict = empresa_serializer.load(data)
        empresa = Empresa(nombre=record_dict['nombre'],
                          usuario_id=record_dict['usuario_id'],
                          rubro_id=record_dict['rubro_id'])
        empresa.descripcion = record_dict['descripcion']
        empresa.save()
        resp = empresa_serializer.dump(empresa)
        return resp, 201


class EmpresaResource(Resource):
    def get(self, id):
        r = Empresa.get_by_id(id)
        if r is None:
            return {"mensaje": "empresa no existe"}, 404
        resp = empresa_serializer.dump(r)
        return resp

    def delete(self, id):
        r = Empresa.get_by_id(id)
        if r is None:
            return {"mensaje": "empresa no existe"}, 500
        empresas = db.session.delete(r)
        db.session.commit()
        return '', 204

    def put(self, id):
        r = Empresa.get_by_id(id)
        if r is None:
            return {"message": "No se encontro Id", "data": id}, 404

        data = request.get_json()
        record_dict = empresa_serializer.load(data)

        r.nombre = record_dict['nombre']
        r.descripcion = record_dict['descripcion']
        r.ciudad = record_dict['ciudad']
        r.frase = record_dict['frase']
        r.direccion = record_dict['direccion']
        r.telefono = record_dict['telefono']

        rubro = Rubro.get_by_id(record_dict['rubro']['id'])
        if rubro is None:
            return {"message": "No existe Rubro Id", "data": id}, 404
        r.rubro_id = record_dict['rubro']['id']

        u = User.get_by_id(record_dict['usuario']['id'])
        if u is None:
            return {"message": "No existe Usuario Id", "data": id}, 404
        r.user_id = record_dict['usuario']['id']

        r.save()
        resp = empresa_serializer.dump(r)
        return {"message": "Actualizado Ok", "data": resp}, 200

api.add_resource(EmpresaListResource, '/api/v1.0/empresas',endpoint='empresas_list_resource')
api.add_resource(EmpresaResource, '/api/v1.0/empresas/<int:id>', endpoint='empresa_resource')
