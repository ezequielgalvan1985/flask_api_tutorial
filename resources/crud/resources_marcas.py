import json

import pika

from extensiones import ma
from marshmallow import fields
from flask import request, Blueprint
from flask_restful import Api, Resource

from schemas import MarcaSchema
from models import Marca
from db import db
import sys
import pickle

marca_serializer = MarcaSchema()
marcas_blueprint = Blueprint('marcas_blueprint', __name__)
api = Api(marcas_blueprint)


class MarcaRepository():
    def add(self, data):
        record_dict = marca_serializer.load(data)
        marca = Marca(nombre=record_dict['nombre'], descripcion=record_dict['descripcion'])
        marca.save()
        return 0

    def list(self):
        marcas = db.session.execute(db.select(Marca).order_by(Marca.nombre)).scalars()
        result = marca_serializer.dump(marcas, many=True)
        return result


class Mediador():
    def __init__(self):
        self.marcas_gestor=MarcaGestor()

    def publicar(self,comando:object, evento:str):
        if(evento=='marcas_create'):
            self.marcas_gestor.publish_create(comando)


class MarcaGestor():
    def publish_create(self, body):
        connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        channel = connection.channel()
        queue_name = 'marcas_create_queue_4'
        channel.queue_declare(queue=queue_name, durable=True)
        channel.basic_publish(exchange='', body=body,routing_key='marcas_create_queue_4')
        print(f" [x] Sent publish_create_marca")
        connection.close()

class MarcaListResource(Resource):
    def __init__(self):
        self.repo=MarcaRepository()
        self.mediador= Mediador()

    def get(self):
        return self.repo.list()

    def post(self):
        data = request.get_json()
        #record_dict = marca_serializer.load(data)
        #marca = Marca(nombre=record_dict['nombre'],descripcion=record_dict['descripcion'])
        body = pickle.dumps(data)
        self.mediador.publicar(body,'marcas_create')
        return "creado ok", 201



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
