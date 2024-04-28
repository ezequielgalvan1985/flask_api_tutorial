import json

from flask import request, Blueprint
from flask_restful import Api, Resource

from schemas import MarcaSchema
from models import Marca
from db import db
import sys
import pika
import pickle

marca_serializer = MarcaSchema()
marcas_blueprint = Blueprint('marcas_blueprint', __name__)
api = Api(marcas_blueprint)


def publicar(self, queue, body):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
    channel.queue_declare(queue=queue)
    channel.basic_publish(exchange='', routing_key=queue, body=body)
    print(" [x] Sent 'MARCAS'")
    connection.close()

class MarcaListResource(Resource):
    def get(self):
        marcas = db.session.execute(db.select(Marca).order_by(Marca.nombre)).scalars()
        result = marca_serializer.dump(marcas, many=True)
        return result

    def post(self):
        data = request.get_json()
        # convertir a bytes
        body = pickle.dumps(data)
        publicar('marcas_create', body)

        record_dict = marca_serializer.load(data)
        marca = Marca(nombre=record_dict['nombre'],descripcion=record_dict['descripcion'])
        #marca.save()
        resp = marca_serializer.dump(marca)
        return resp, 201



class MarcaResource(Resource):
    def get(self, id):
        r = Marca.get_by_id(id)
        if r is None:
            return {"mensaje": "marca no existe"}, 404
        resp = marca_serializer.dump(r)
        return resp

    def delete(self, id):
        r = Marca.get_by_id(id)
        if r is None:
            return {"mensaje": "marca no existe"}, 500
        marcas = db.session.delete(r)
        db.session.commit()
        return '', 204

    def put(self, id):

        r = Marca.get_by_id(id)
        if r is None:
            return {"message": "No se encontro Id", "data": id}, 404

        data = request.get_json()
        record_dict = marca_serializer.load(data)
        r.nombre = record_dict['nombre']
        r.descripcion = record_dict['descripcion']
        r.save()
        resp = marca_serializer.dump(r)
        return {"message": "Actualizado Ok", "data": resp}, 200

api.add_resource(MarcaListResource, '/api/v1.0/marcas',endpoint='marcas_list_resource')
api.add_resource(MarcaResource, '/api/v1.0/marcas/<int:id>', endpoint='marca_resource')

