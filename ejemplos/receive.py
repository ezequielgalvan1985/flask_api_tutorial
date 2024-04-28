#!/usr/bin/env python
import pika, sys, os,pickle
from schemas import MarcaSchema
from models import Marca


def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='marcas_create')
    channel.queue_declare(queue='marcas_update')
    channel.queue_declare(queue='marcas_delete')

    def marcas_create(ch, method, properties, body):
        registro = pickle.loads(body)
        print(f" [x] Decodificado {registro}")
        marca_serializer = MarcaSchema()
        record_dict = marca_serializer.load(registro)
        marca = Marca(nombre=record_dict['nombre'], descripcion=record_dict['descripcion'])
        marca.save()
        print(f" [x] Guardado OK {registro}")
    def marcas_update(ch, method, properties, body):
        registro = pickle.loads(body)
        print(f" [x] Decodificado {registro}")
        marca_serializer = MarcaSchema()
        record_dict = marca_serializer.load(registro)
        marca = Marca(nombre=record_dict['nombre'], descripcion=record_dict['descripcion'])
        marca.save()
        print(f" [x] Guardado OK {registro}")
    def marcas_delete(ch, method, properties, body):
        registro = pickle.loads(body)
        print(f" [x] Decodificado {registro}")
        marca_serializer = MarcaSchema()
        record_dict = marca_serializer.load(registro)
        marca = Marca(nombre=record_dict['nombre'], descripcion=record_dict['descripcion'])
        marca.save()
        print(f" [x] Guardado OK {registro}")

    channel.basic_consume(queue='marcas_create', on_message_callback=marcas_create, auto_ack=True)
    channel.basic_consume(queue='marcas_update', on_message_callback=marcas_update, auto_ack=True)
    channel.basic_consume(queue='marcas_delete', on_message_callback=marcas_delete, auto_ack=True)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)