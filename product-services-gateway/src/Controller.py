import requests
import asyncio
from flask import jsonify,make_response
import json
from bson import ObjectId
import os
import time
import pika
import uuid
import ast

RABBITMQSERVER = os.environ['AMPQ_HOST']
#PIKAUSERNAME = os.environ['PIKAUSERNAME']
#PIKAPASSWORD = os.environ['PIKAPASSWORD']

#RABBITMQSERVER = 'localhost'
#PIKAUSERNAME = 'user'
#PIKAPASSWORD = 'admin'

class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)

class RabbitRpcClient(object):

    def __init__(self):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=RABBITMQSERVER))

        self.channel = self.connection.channel()

        result = self.channel.queue_declare(queue='', exclusive=True)
        self.callback_queue = result.method.queue

        self.channel.basic_consume(
            queue=self.callback_queue,
            on_message_callback=self.on_response,
            auto_ack=True)

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body

    def call(self, n,queue_name):
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(
            exchange='',
            routing_key=queue_name,
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.corr_id,
            ),
            body=str(n))
        while self.response is None:
            self.connection.process_data_events()


        return self.response



async def getProductInfo(pid):
        
    try:

        rpc = RabbitRpcClient()
        v = rpc.call(pid,'product-info-service-q')
        
        v=v.decode('utf-8')
        v=json.dumps({"productInfo":json.loads(json.dumps(v))})
        v=json.loads(v)

    except IOError as err:
        print("IOError: {0}".format(err))
 
    return v

async def getProductReviewService(pid):
    #start_time = time.time()
        
    try:
        rpc = RabbitRpcClient()
        v = rpc.call(pid,'product-review-service-q')
        
        v=v.decode('utf-8')

        v = json.dumps({"Product_Review":json.loads(json.dumps(v))})
        v = json.loads(v)

    except IOError as err:
        print("IOError: {0}".format(err))
 
    return v

async def getProductRecommendationService(pid):
    #start_time = time.time()
        
    try:
        rpc = RabbitRpcClient()
        v = rpc.call(pid,'product-review-service-q')
        
        v=v.decode('utf-8')

        v = json.dumps({"Product_Review":json.loads(json.dumps(v))})
        v = json.loads(v)

    except IOError as err:
        print("IOError: {0}".format(err))
 
    return v

async def getProductShoppingCartService(cid):
    #start_time = time.time()
        
    try:
        rpc = RabbitRpcClient()
        v = rpc.call(cid,'customer-shopping-cart-q')
        
        v=v.decode('utf-8')

        v = json.dumps({"Shopping_Cart":json.loads(json.dumps(v))})
        v = json.loads(v)

    except IOError as err:
        print("IOError: {0}".format(err))
 
    return v

async def getProductShippingService(pid):
    #start_time = time.time()
        
    try:
        rpc = RabbitRpcClient()
        v = rpc.call(pid,'product-shipping-service-q')
        
        v=v.decode('utf-8')

        v = json.dumps({"Shipping":json.loads(json.dumps(v))})
        v = json.loads(v)

    except IOError as err:
        print("IOError: {0}".format(err))
 
    return v




async def main(product_id,customer_id):
    values = await asyncio.gather(*[getProductInfo(product_id),getProductReviewService(product_id),getProductRecommendationService(product_id),getProductShoppingCartService(customer_id),getProductShippingService(product_id)])
    return JSONEncoder().encode(values)

def doTheMagic(product_id,customer_id):

    retval = asyncio.run(main(product_id,customer_id))

    return retval

