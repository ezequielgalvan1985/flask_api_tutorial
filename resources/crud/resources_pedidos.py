from flask import request, Blueprint, abort
from flask_jwt_extended import jwt_required, get_jwt
from flask_restful import Api, Resource
from sqlalchemy import desc

from schemas import PedidoSchema, RolPermisoSchema, PedidoFindByUserEmpresaRequestSchemaDto, PedidoItemSchemaDto, \
    PedidoItemSchema, PedidoSchemaDto
from models import Pedido, Permiso, Empresa, User, Producto, Pedidoitem
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
        responseDto = PedidoSchemaDto()
        resp = responseDto.dump(pedido)
        return resp, 201


class PedidoResource(Resource):
    def get(self, id):
        r = Pedido.get_by_id(id)
        if r is None:
            return {"mensaje": "pedido no existe"}, 404
        responseDto = PedidoSchemaDto()
        resp = responseDto.dump(r)

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
        responseDto = PedidoSchemaDto()
        resp = responseDto.dump(pedido)
        return {"message": "Actualizado Ok", "data": resp}, 200


api.add_resource(PedidoListResource, '/api/v1.0/pedidos',endpoint='pedidos_list_resource')
api.add_resource(PedidoResource, '/api/v1.0/pedidos/<int:id>', endpoint='pedido_resource')

#======================
#METODOS PERSONALIZADOS
#======================

pedido_serializer = PedidoSchema()
pedidos_getultimopendiente_blueprint = Blueprint('pedidos_getultimopendiente_blueprint', __name__)

@pedidos_getultimopendiente_blueprint.route("/api/v1.0/pedidos/consultas/getultimopendiente/<int:user_id>", methods=["GET"])
@jwt_required()
def getUltimoPendiente(user_id):
    r=Pedido.query.filter_by(user_id=user_id, estado="I").order_by(desc(Pedido.id)).first()
    #r = db.session.execute(db.select(Pedido).order_by(Pedido.id)).first()

    if r is None:
        return abort(500, "No existe Pedido para el Usuario "+ user_id)
    resp = pedido_serializer.dump(r, many=False)
    return resp, 200



pedidos_pendientesfindbyuser_blueprint = Blueprint('pedidos_pendientesfindbyuser_blueprint', __name__)
@pedidos_pendientesfindbyuser_blueprint.route("/api/v1.0/pedidos/consultas/findpendientesbyuser/<int:user_id>", methods=["GET"])
@jwt_required()
def pendientesFindByUser(user_id):
    r=Pedido.query.filter_by(user_id=user_id, estado="I").order_by(desc(Pedido.id)).all()
    if r is None:
        return abort(500, "No existe Pedido para el Usuario "+ user_id)
    pedido_serializer = PedidoSchemaDto()
    resp = pedido_serializer.dump(r, many=True)
    return resp, 200


pedidos_findbyuser_blueprint = Blueprint('pedidos_findbyuser_blueprint', __name__)
@pedidos_findbyuser_blueprint.route("/api/v1.0/pedidos/consultas/getbyuser/<int:user_id>", methods=["GET"])
@jwt_required()
def findByUser(user_id):
    r=Pedido.query.filter_by(user_id=user_id).order_by(desc(Pedido.id)).all()
    if r is None:
        return abort(500, "No existe Pedido para el Usuario "+ user_id)
    resp = pedido_serializer.dump(r, many=True)
    return resp, 200



pedidos_findultpendbyuserandempresa_blueprint = Blueprint('pedidos_findultpendbyuserandempresa_blueprint', __name__)
@pedidos_findultpendbyuserandempresa_blueprint.route("/api/v1.0/pedidos/consultas/findultpendbyuserandempresa", methods=["POST"])
@jwt_required()
def findUltPendByUserAndEmpresa():
    data = request.get_json()
    serializer = PedidoFindByUserEmpresaRequestSchemaDto()
    d = serializer.load(data)
    if d['user_id'] is None:
        return abort(500, "No existe Usuario ")
    if d['empresa_id'] is None:
        return abort(500, "No existe Empresa ")

    r=Pedido.query.filter_by(user_id=d['user_id'], empresa_id=d['empresa_id']).order_by(desc(Pedido.id)).all()
    if r is None:
        return abort(500, "No existe Pedido para el Usuario ")
    responseDto = PedidoSchemaDto()
    resp = responseDto.dump(r, many=True)
    return resp, 200



pedidos_insertitempedido_blueprint = Blueprint('pedidos_insertitempedido_blueprint', __name__)
@pedidos_insertitempedido_blueprint.route("/api/v1.0/pedidoitems", methods=["POST"])
@jwt_required()
def insertItemPedido():
    data = request.get_json()
    serializer = PedidoItemSchema()
    d = serializer.load(data)
    p = Producto.get_by_id(d['producto']['id'])
    if p is None:
        return abort(500, "No existe Producto")
    pedido = Pedido.get_by_id(d['pedido']['id'])
    if pedido is None:
        return abort(500, "No existe Pedido")
    if d['cantidad'] <= 0:
        return abort(500, "Cantidad debe ser mayor a 0")
    i = Pedidoitem()
    i.pedido = pedido
    i.producto = p
    i.cantidad = d['cantidad']
    i.save()
    pedido.get_by_id(pedido.id)
    responseDto = PedidoItemSchemaDto()
    responseDto.dump(pedido)
    resp = pedido_serializer.dump(responseDto, many=False)
    return resp, 200
