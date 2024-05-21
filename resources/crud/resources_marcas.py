import json

import pika

from extensiones import ma
from marshmallow import fields
from flask import request, Blueprint
from flask_restful import Api, Resource

from repository.repositories import MarcaRepository
from schemas import MarcaSchema
from models import Marca
from db import db
import sys
import pickle

marca_serializer = MarcaSchema()
marcas_blueprint = Blueprint('marcas_blueprint', __name__)
api = Api(marcas_blueprint)




class MarcaGestor():
    def publicar(self, body, method):
        connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        channel = connection.channel()
        properties = pika.BasicProperties(method)
        queue_name = 'marcas_crud'
        channel.queue_declare(queue=queue_name, durable=True)
        channel.basic_publish(exchange='', body=body,routing_key=queue_name,properties=properties)
        print(f" [x] Sent "+method + " to "+queue_name )
        connection.close()



class MarcaListResource(Resource):
    def __init__(self):
        self.repo=MarcaRepository()
        self.gestor= MarcaGestor()

    def get(self):
        return self.repo.list()

    def post(self):
        #data = request.get_json()
        #record_dict = marca_serializer.load(data)
        #marca = Marca(nombre=record_dict['nombre'], descripcion=record_dict['descripcion'])
        #marca.save()
        result = self.repo.create(request.get_json())
        #self.gestor.publicar(pickle.dumps(request.get_json()),'marca_create')
        return result, 201



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
