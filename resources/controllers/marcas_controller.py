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

class MarcaController():
    def create(self, data):

        record_dict = marca_serializer.load(data)
        marca = Marca(nombre=record_dict['nombre'],descripcion=record_dict['descripcion'])
        marca.save()
        resp = marca_serializer.dump(marca)
        return 0


