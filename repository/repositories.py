from schemas import MarcaSchema
from models import Marca
from db import db
import sys
import pika
import pickle

marca_serializer = MarcaSchema()

class MarcaRepository():
    def create(self, data):
        record_dict = marca_serializer.load(data)
        marca = Marca(nombre=record_dict['nombre'], descripcion=record_dict['descripcion'])
        marca.save()
        return marca

    def update(self,data):
        r = Marca.get_by_id(id)
        if r is None:
            return {"message": "No se encontro Id", "data": id}, 404
        record_dict = marca_serializer.load(data)
        r.nombre = record_dict['nombre']
        r.descripcion = record_dict['descripcion']
        r.save()
        resp = marca_serializer.dump(r)
        return {"message": "Actualizado Ok", "data": resp}, 200

    def list(self):
        marcas = db.session.execute(db.select(Marca).order_by(Marca.nombre)).scalars()
        result = marca_serializer.dump(marcas, many=True)
        return result
