#!/usr/bin/env python
import json
import pickle
import pika
import http.client

from app import app
from models import Marca
from schemas import MarcaSchema

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()
exchange_name = ''
queue_name = 'marcas_create_queue_4'
channel.queue_declare(queue=queue_name, durable=True)

marca_serializer = MarcaSchema()


def marcas_create_callback(ch, method, properties, body):
    try:
        print("marcas_create_callback")
        body = pickle.loads(body)
        with app.app_context():
            record_dict = marca_serializer.load(body)
            marca = Marca(nombre=record_dict['nombre'], descripcion=record_dict['descripcion'])
            marca.save()
            print(body)

    except:
        print("Error al dar de alta: ")

channel.basic_consume(queue=queue_name, on_message_callback=marcas_create_callback)
print('... Worker Marcas creado')
channel.start_consuming()

