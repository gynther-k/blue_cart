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
PIKAUSERNAME = os.environ['PIKAUSERNAME']
PIKAPASSWORD = os.environ['PIKAPASSWORD']

uri = "mongodb+srv://"+os.environ['MONGO_DB_USERNAME']+":"+os.environ['MONGO_DB_PASSWORD']+"@"+os.environ['MONGO_DB_CLUSTER_ADDRESS']+"?retryWrites=true&w=majority"
#uri = "mongodb+srv://gynther:admin@cluster0.ypo7l.azure.mongodb.net/products?retryWrites=true&w=majority"
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
    pika.ConnectionParameters(host=RABBITMQSERVER))

channel = connection.channel()

channel.queue_declare(queue='product-review-service-q')

def on_request(ch, method, props, body):
    pid = int(body)

    response = Controller.retrieve_review_By_Product_Id(mongodbconnection,str(pid))

    ch.basic_publish(exchange='',
                     routing_key=props.reply_to,
                     properties=pika.BasicProperties(correlation_id = \
                                                         props.correlation_id),
                     body=str(response))
    ch.basic_ack(delivery_tag=method.delivery_tag)

channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='product-review-service-q', on_message_callback=on_request)

print(" [x] Awaiting RPC requests")
channel.start_consuming()


