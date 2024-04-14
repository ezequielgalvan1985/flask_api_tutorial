from flask import request, Blueprint, abort
from flask_jwt_extended import jwt_required, get_jwt
from flask_restful import Api, Resource
from schemas import PedidoSchema, RolPermisoSchema
from models import Pedido, Permiso, Empresa, User
from db import db
from flask_jwt_extended import get_jwt_identity
import json

pedido_serializer = PedidoSchema()
pedidos_blueprint = Blueprint('pedidos_blueprint', __name__)
api = Api(pedidos_blueprint)


class PedidoListResource(Resource):
    def get(self):
        pedidos = db.session.execute(db.select(Pedido).order_by(Pedido.id)).scalars()
        result = pedido_serializer.dump(pedidos, many=True)
        return result

    def post(self):
        data = request.get_json()
        record_dict = pedido_serializer.load(data)
        pedido = Pedido(record_dict['fecha'])
        pedido.estado = record_dict['estado']
        pedido.importeenvio = record_dict['importeenvio']
        pedido.direccion = record_dict['direccion']
        pedido.empresa = Empresa.get_by_id(record_dict['empresa']['id'])
        pedido.user = User.get_by_id(record_dict['user']['id'])

        pedido.save()
        resp = pedido_serializer.dump(pedido)
        return resp, 201


class PedidoResource(Resource):
    def get(self, id):
        r = Pedido.get_by_id(id)
        if r is None:
            return {"mensaje": "pedido no existe"}, 404
        resp = pedido_serializer.dump(r)
        return resp

    def delete(self, id):
        r = Pedido.get_by_id(id)
        if r is None:
            return {"mensaje": "pedido no existe"}, 500
        pedidos = db.session.delete(r)
        db.session.commit()
        return '', 204

    def put(self, id):
        pedido = Pedido.get_by_id(id)
        if pedido is None:
            return {"message": "No se encontro Id", "data": id}, 404

        data = request.get_json()
        record_dict = pedido_serializer.load(data)

        pedido.estado = record_dict['estado']
        pedido.importeenvio = record_dict['importeenvio']
        pedido.direccion = record_dict['direccion']
        pedido.empresa = Empresa.get_by_id(record_dict['empresa']['id'])
        pedido.user = User.get_by_id(record_dict['user']['id'])

        pedido.save()
        resp = pedido_serializer.dump(pedido)
        return {"message": "Actualizado Ok", "data": resp}, 200


api.add_resource(PedidoListResource, '/api/v1.0/pedidos',endpoint='pedidos_list_resource')
api.add_resource(PedidoResource, '/api/v1.0/pedidos/<int:id>', endpoint='pedido_resource')
