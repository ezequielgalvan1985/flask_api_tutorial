from enum import Enum

from flask import request, Blueprint, abort
from flask_jwt_extended import jwt_required, get_jwt
from flask_restful import Api, Resource
from sqlalchemy import desc
from schemas import PedidoSchema, RolPermisoSchema, PedidoFindByUserEmpresaRequestSchemaDto, PedidoItemSchemaDto, \
    PedidoItemSchema, PedidoSchemaDto, PedidoItemUpdRequestSchemaDto, VentasPorProductosSchemaDto, \
    PedidoFindByEmpresaAndEstadoRequestDto
from models import Pedido, Permiso, Empresa, User, Producto, Pedidoitem
from db import db
from flask_jwt_extended import get_jwt_identity
import json

class Estados(Enum):
    PENDIENTE=0
    CONFIRMADO=1
    ENPREPARACION=2
    PREPARADO=3
    ENCAMINO=4
    ENTREGADO=5


pedido_serializer = PedidoSchema()
pedidos_blueprint = Blueprint('pedidos_blueprint', __name__)
api = Api(pedidos_blueprint)


class PedidoListResource(Resource):
    def get(self):
        pedidos = db.session.execute(db.select(Pedido).order_by(Pedido.id)).scalars()
        pedido_serializer = PedidoSchema()
        result = pedido_serializer.dump(pedidos, many=True)
        return result

    def post(self):
        try:
            data = request.get_json()
            pedido_serializer = PedidoSchemaDto()
            record_dict = pedido_serializer.load(data)
            pedido = Pedido(record_dict['fecha'])
            pedido.estado = record_dict['estado']
            pedido.importeenvio = record_dict['importeenvio']
            pedido.direccion = record_dict['direccion']
            pedido.empresa = Empresa.get_by_id(record_dict['empresa']['id'])
            pedido.user = User.get_by_id(record_dict['usuario']['id'])

            pedido.save()
            responseDto = PedidoSchemaDto()
            resp = responseDto.dump(pedido)

            return pedido.id, 201
        except BaseException as e:
            return {"message":"Error "+ str(e)},500

class PedidoResource(Resource):
    def get(self, id):
        r = Pedido.get_by_id(id)
        if r is None:
            return {"mensaje": "pedido no existe"}, 404
        responseDto = PedidoSchema()
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
    print("estado: "+str(Estados.PENDIENTE.value) )
    r=Pedido.query.filter_by(user_id=user_id, estado=str(Estados.PENDIENTE.value)).order_by(desc(Pedido.id)).first()
    if r is None:
        return {"message":"No existe Pedido para el Usuario "+ str(user_id)},200
    resp = pedido_serializer.dump(r, many=False)
    return resp, 200



pedidos_pendientesfindbyuser_blueprint = Blueprint('pedidos_pendientesfindbyuser_blueprint', __name__)
@pedidos_pendientesfindbyuser_blueprint.route("/api/v1.0/pedidos/consultas/findpendientesbyuser/<int:user_id>", methods=["GET"])
@jwt_required()
def pendientesFindByUser(user_id):
    r=Pedido.query.filter_by(user_id=user_id, estado=str(Estados.PENDIENTE.value)).order_by(desc(Pedido.id)).all()
    if r is None:
        return {"message":"No existe Pedido para el Usuario "+ user_id},500
    pedido_serializer = PedidoSchemaDto()
    resp = pedido_serializer.dump(r, many=True)
    return resp, 200


pedidos_findbyuser_blueprint = Blueprint('pedidos_findbyuser_blueprint', __name__)
@pedidos_findbyuser_blueprint.route("/api/v1.0/pedidos/consultas/usuario/<int:user_id>", methods=["GET"])
@jwt_required()
def findByUser(user_id):
    r=Pedido.query.filter_by(user_id=user_id).order_by(desc(Pedido.id)).all()
    if r is None:
        return {"message":"No existe Pedido para el Usuario "+ user_id},500
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
        return {"message": "No existe Usuario"}, 500
    if d['empresa_id'] is None:
        return {"message": "No existe Empresa"}, 500
    r=Pedido.query.filter_by(user_id=d['user_id'], empresa_id=d['empresa_id'],estado=Estados.PENDIENTE.value).order_by(desc(Pedido.id)).all()
    if r is None:
        return {"message": "No existe Pedido para el Usuario"}, 500
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
        return {"message": "No existe Producto"}, 500
    pedido = Pedido.get_by_id(d['pedido']['id'])
    if pedido is None:
        return {"message": "No existe Pedido"}, 500
    if d['cantidad'] <= 0:
        return {"message": "Cantidad debe ser mayor a 0"}, 500
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



pedidoitem_updcantidad_blueprint = Blueprint('pedidoitem_updrequestdto_blueprint', __name__)
@pedidoitem_updcantidad_blueprint.route("/api/v1.0/pedidoitems/accion/upd/cantidad", methods=["POST"])
@jwt_required()
def pedidoitem_upd_cantidad():
    data = request.get_json()
    serializer = PedidoItemUpdRequestSchemaDto()
    d = serializer.load(data)
    i = Pedidoitem.get_by_id(d['id'])
    if i is None:
        return abort(500, "No existe PedidoItem")
    if d['cantidad'] <= 0:
        return abort(500, "Cantidad debe ser mayor a 0")
    i.cantidad = d['cantidad']
    i.save()
    responseDto = PedidoItemSchemaDto()
    resp = responseDto.dump(i, many=False)
    return resp, 200


pedidos_updestado_blueprint = Blueprint('pedidos_updestado_blueprint', __name__)
@pedidos_updestado_blueprint.route("/api/v1.0/pedidos/accion/upd/estado", methods=["PATCH"])
@jwt_required()
def pedidos_upd_cantidad():
    data = request.get_json()
    serializer = PedidoSchemaDto()
    d = serializer.load(data)
    r = Pedido.get_by_id(d['id'])
    if r is None:
        return abort(500, "No existe PedidoItem")
    r.estado = d['estado']
    r.save()
    resp = serializer.dump(r, many=False)
    return resp, 200


ventas_productos_blueprint = Blueprint('ventas_productos_blueprint', __name__)
@pedidos_updestado_blueprint.route("/api/v1.0/ventas/consulta/productos", methods=["POST"])
@jwt_required()
def ventas_get_productos():
    data = request.get_json()
    serializer = VentasPorProductosSchemaDto()
    d = serializer.load(data)
    r = Pedido.query.filter_by(empresa_id = d['empresa_id']).all()
    if r is None:
        return {"message":"No existe PedidoItem"},500
    resp = serializer.dump(r, many=False)
    return resp, 200



pedidos_findbyempresaandestado_blueprint = Blueprint('pedidos_findbyempresaandestado_blueprint', __name__)
@pedidos_findbyempresaandestado_blueprint.route("/api/v1.0/pedidos/consultas/empresa/estado", methods=["POST"])
@jwt_required()
def findbyempresaandestado():
    data = request.get_json()
    requestDto = PedidoFindByEmpresaAndEstadoRequestDto()
    d = requestDto.load(data)

    e = Empresa.query.filter_by(user_id=d['usuario_id']).first()
    if e is None:
        return {"message": "Usuario no tiene Empresa asignada"}, 500

    r = Pedido.query.filter_by(empresa_id=e.id, estado=d['estado_id']).all()
    if r is None:
        return {"message":"No existen Pedidos"},500

    responseDto = PedidoSchemaDto()
    resp = responseDto.dump(r, many=True)
    return resp, 200
