#!/usr/bin/env python
import pika
import sys

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='direct_logs', exchange_type='direct')
result = channel.queue_declare(queue='logs_error_queue', exclusive=True)
queue_name = result.method.queue

channel.queue_bind(exchange='direct_logs', queue=queue_name, routing_key='error')

print(' [*] Waiting for logs Errores. To exit press CTRL+C')


def callback(ch, method, properties, body):
    print(f" [x] {method.routing_key}:{body}")


channel.basic_consume(
    queue=queue_name, on_message_callback=callback, auto_ack=True)

channel.start_consuming()