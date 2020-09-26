import Controller
from pymongo import MongoClient 
from flask import jsonify
import os
import json
from bson import ObjectId
import pika

RABBITMQSERVER = os.environ['AMPQ_HOST']

uri = "mongodb+srv://"+os.environ['MONGO_DB_USERNAME']+":"+os.environ['MONGO_DB_PASSWORD']+"@"+os.environ['MONGO_DB_CLUSTER_ADDRESS']+"?retryWrites=true&w=majority"
conn='null'
mongodbconnection='null'

try: 
    conn = MongoClient(uri)
    mongodbconnection = conn.products #database name
except Exception as err:
    print("Exception in mongoDB: {0}".format(err))


class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host=RABBITMQSERVER,credentials=pika.PlainCredentials('guest','guest')))

channel = connection.channel()

channel.queue_declare(queue='product-info-service-q')

def on_request(ch, method, props, body):
    pid = int(body)

    response = Controller.retrieve_Product_By_Id(mongodbconnection,pid)

    ch.basic_publish(exchange='',
                     routing_key=props.reply_to,
                     properties=pika.BasicProperties(correlation_id = \
                                                         props.correlation_id),
                     body=str(response))
    ch.basic_ack(delivery_tag=method.delivery_tag)

channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='product-info-service-q', on_message_callback=on_request)

print(" [x] Awaiting RPC requests")
channel.start_consuming()


