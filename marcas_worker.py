#!/usr/bin/env python
import json
import pickle
import pika
from app import app
from models import Marca
from repository.repositories import MarcaRepository
from schemas import MarcaSchema

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()
exchange_name = ''
queue_name = 'marcas_crud'
channel.queue_declare(queue=queue_name, durable=True)

marca_serializer = MarcaSchema()
repository = MarcaRepository()

def marcas_crud_callback(ch, method, properties, body):
    try:
        print("marcas_crud_callback")
        json_data = pickle.loads(body)
        with app.app_context():
            if properties.content_type == 'marca_create':
                repository.add(json_data)
            elif properties.content_type == 'marca_update':
                repository.update(json_data)

    except:
        print("Error crud marcas")

channel.basic_consume(queue=queue_name, on_message_callback=marcas_crud_callback)
print('... Worker Marcas Crud escuchando...')
channel.start_consuming()

