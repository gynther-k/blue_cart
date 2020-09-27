import Controller
from pymongo import MongoClient 
from flask import jsonify
import os
import json
from bson import ObjectId
import pika
import amqpstorm
from amqpstorm import Message

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

def on_request(message):

    cid = str(int(message.body))

    response = str(Controller.retrieve_shopping_cart_by_customer_id(mongodbconnection,cid))

    properties = {
        'correlation_id': message.correlation_id
    }

    response = Message.create(message.channel, response, properties)
    response.publish(message.reply_to)

    message.ack()
    

CONNECTION = amqpstorm.Connection(RABBITMQSERVER, 'guest', 'guest')
CHANNEL = CONNECTION.channel()

CHANNEL.queue.declare(queue='customer-shopping-cart-q')
CHANNEL.basic.qos(prefetch_count=1)
CHANNEL.basic.consume(on_request, queue='customer-shopping-cart-q')

print(" [x] Awaiting RPC requests")
CHANNEL.start_consuming()
