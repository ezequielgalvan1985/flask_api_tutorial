#!/usr/bin/env python
import sys
import pika

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()
channel.queue_declare(queue='hello')

message = ' '.join(sys.argv[1:]) or "Hello World!"

channel.basic_publish(exchange='', routing_key='cola_prueba', body='Hello World!')
print(" [x] Sent 'Hello World!'")
connection.close()