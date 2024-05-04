from schemas import MarcaSchema
from models import Marca
from db import db
import sys
import pika
import pickle

marca_serializer = MarcaSchema()

class MarcaRepository():
    def create(self,data):
        record_dict = marca_serializer.load(data)
        marca = Marca(nombre=record_dict['nombre'], descripcion=record_dict['descripcion'])
        marca.save()
        return 0
