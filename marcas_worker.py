#!/usr/bin/env python
import pika

from resources.crud.resources_marcas import MarcaRepository

class MarcaWorker():
    def __init__(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        self.channel = self.connection.channel()
        self.exchange_name = 'marcas'
        self.queue_name = 'marcas_create_queue'
        self.channel.exchange_declare(exchange=self.exchange_name, exchange_type='direct')
        result = self.channel.queue_declare(queue=self.queue_name, exclusive=True)
        self.channel.queue_bind(exchange=self.exchange_name, queue=self.queue_name)
        self.channel.basic_consume(queue=self.queue_name, on_message_callback=self.marcas_create_callback, auto_ack=True)

    def marcas_create_callback(ch, method, properties, body):
        m = MarcaRepository()
        if (m.create(body) == 0):
            print(f" [x] Creado OK {body}")
        else:
            print(f" [x] Creado Con Error {body}")

    def run(self):
        self.channel.start_consuming()
        print(' [*] Waiting for logs Marcas. To exit press CTRL+C')

