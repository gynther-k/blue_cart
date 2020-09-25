import Controller
from pymongo import MongoClient 
from flask import jsonify
import os
import json
from bson import ObjectId
import pika

#RABBITMQSERVER = 'rabbit@mu-rabbit-rabbitmq-0.mu-rabbit-rabbitmq-headless.rabbit.svc.cluster.local'
#RABBITMQSERVER = 'localhost'    
#PIKAUSERNAME = 'user'
#PIKAPASSWORD = 'admin'

RABBITMQSERVER = os.environ['AMPQ_HOST']
#PIKAUSERNAME = os.environ['PIKAUSERNAME']
#PIKAPASSWORD = os.environ['PIKAPASSWORD']


class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)
print("START SHIPPING SERVER BEFORE CONNECTION")
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host=RABBITMQSERVER,credentials=pika.PlainCredentials('guest','guest')))

print(connection)
print("AFTER CONNECTION")


channel = connection.channel()

channel.queue_declare(queue='product-shipping-service-q')

def on_request(ch, method, props, body):
    pid = int(body)

    response = Controller.retrieve_shipping()

    ch.basic_publish(exchange='',
                     routing_key=props.reply_to,
                     properties=pika.BasicProperties(correlation_id = \
                                                         props.correlation_id),
                     body=str(response))
    ch.basic_ack(delivery_tag=method.delivery_tag)

channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='product-shipping-service-q', on_message_callback=on_request)

print(" [x] Awaiting RPC requests")
channel.start_consuming()


