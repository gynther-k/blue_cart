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
import threading
from time import sleep
import amqpstorm
from amqpstorm import Message


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


class RpcClient(object):
    """Asynchronous Rpc client."""

    def __init__(self, host, username, password, rpc_queue):
        self.queue = {}
        self.host = host
        self.username = username
        self.password = password
        self.channel = None
        self.connection = None
        self.callback_queue = None
        self.rpc_queue = rpc_queue
        self.open()

    def open(self):
        """Open Connection."""
        self.connection = amqpstorm.Connection(self.host, self.username,
                                               self.password)
        self.channel = self.connection.channel()
        self.channel.queue.declare(self.rpc_queue)
        result = self.channel.queue.declare(exclusive=True)
        self.callback_queue = result['queue']
        self.channel.basic.consume(self._on_response, no_ack=True,
                                   queue=self.callback_queue)
        self._create_process_thread()

    def _create_process_thread(self):
        """Create a thread responsible for consuming messages in response
        RPC requests.
        """
        thread = threading.Thread(target=self._process_data_events)
        thread.setDaemon(True)
        thread.start()

    def _process_data_events(self):
        """Process Data Events using the Process Thread."""
        self.channel.start_consuming()

    def _on_response(self, message):
        """On Response store the message with the correlation id in a local
        dictionary.
        """
        self.queue[message.correlation_id] = message.body

    def send_request(self, payload):
        # Create the Message object.
        message = Message.create(self.channel, payload)
        message.reply_to = self.callback_queue

        # Create an entry in our local dictionary, using the automatically
        # generated correlation_id as our key.
        self.queue[message.correlation_id] = None

        # Publish the RPC request.
        message.publish(routing_key=self.rpc_queue)

        # Return the Unique ID used to identify the request.
        return message.correlation_id

RPC_CLIENT_PRODUCT = RpcClient(RABBITMQSERVER, 'guest', 'guest', 'product-info-service-q')
RPC_CLIENT_REVIEW = RpcClient(RABBITMQSERVER, 'guest', 'guest', 'product-review-service-q')
RPC_CLIENT_RECOMMENDATION = RpcClient(RABBITMQSERVER, 'guest', 'guest', 'product-recommendation-service-q')
RPC_CLIENT_CART = RpcClient(RABBITMQSERVER, 'guest', 'guest', 'customer-shopping-cart-q')
RPC_CLIENT_SHIPPING = RpcClient(RABBITMQSERVER, 'guest', 'guest', 'product-shipping-service-q')

async def getProductInfo(pid):
        
    try:

        # Send the request and store the requests Unique ID.
        corr_id = RPC_CLIENT_PRODUCT.send_request(pid)

        # Wait until we have received a response.
        # TODO: Add a timeout here and clean up if it fails!
        while RPC_CLIENT_PRODUCT.queue[corr_id] is None:
            sleep(0.1)

        # Return the response to the user.
        v=RPC_CLIENT_PRODUCT.queue.pop(corr_id)
        
        v=v.decode('utf-8')
        v=json.dumps({"productInfo":json.loads(json.dumps(v))})
        v=json.loads(v)

    except IOError as err:
        print("IOError: {0}".format(err))
 
    return v

async def getProductReviewService(pid):
    #start_time = time.time()
        
    try:
        # Send the request and store the requests Unique ID.
        corr_id = RPC_CLIENT_REVIEW.send_request(pid)

        # Wait until we have received a response.
        # TODO: Add a timeout here and clean up if it fails!
        while RPC_CLIENT_REVIEW.queue[corr_id] is None:
            sleep(0.1)

        # Return the response to the user.
        v=RPC_CLIENT_REVIEW.queue.pop(corr_id)
        
        v=v.decode('utf-8')
        v=json.dumps({"productInfo":json.loads(json.dumps(v))})
        v=json.loads(v)

    except IOError as err:
        print("IOError: {0}".format(err))
 
    return v

async def getProductRecommendationService(pid):
    #start_time = time.time()
        
    try:
        # Send the request and store the requests Unique ID.
        corr_id = RPC_CLIENT_RECOMMENDATION.send_request(pid)

        # Wait until we have received a response.
        # TODO: Add a timeout here and clean up if it fails!
        while RPC_CLIENT_RECOMMENDATION.queue[corr_id] is None:
            sleep(0.1)

        # Return the response to the user.
        v=RPC_CLIENT_RECOMMENDATION.queue.pop(corr_id)
        
        v=v.decode('utf-8')
        v=json.dumps({"productInfo":json.loads(json.dumps(v))})
        v=json.loads(v)

    except IOError as err:
        print("IOError: {0}".format(err))
 
    return v

async def getProductShoppingCartService(cid):
    #start_time = time.time()
        
    try:
        # Send the request and store the requests Unique ID.
        corr_id = RPC_CLIENT_CART.send_request(cid)

        # Wait until we have received a response.
        # TODO: Add a timeout here and clean up if it fails!
        while RPC_CLIENT_CART.queue[corr_id] is None:
            sleep(0.1)

        # Return the response to the user.
        v=RPC_CLIENT_CART.queue.pop(corr_id)
        
        v=v.decode('utf-8')
        v=json.dumps({"productInfo":json.loads(json.dumps(v))})
        v=json.loads(v)

    except IOError as err:
        print("IOError: {0}".format(err))
 
    return v

async def getProductShippingService(pid):
    #start_time = time.time()
        
    try:
        # Send the request and store the requests Unique ID.
        corr_id = RPC_CLIENT_SHIPPING.send_request(pid)

        # Wait until we have received a response.
        # TODO: Add a timeout here and clean up if it fails!
        while RPC_CLIENT_SHIPPING.queue[corr_id] is None:
            sleep(0.1)

        # Return the response to the user.
        v=RPC_CLIENT_SHIPPING.queue.pop(corr_id)
        
        v=v.decode('utf-8')
        v=json.dumps({"productInfo":json.loads(json.dumps(v))})
        v=json.loads(v)

    except IOError as err:
        print("IOError: {0}".format(err))
 
    return v




async def main(product_id,customer_id):
    values = await asyncio.gather(*[getProductInfo(product_id),getProductReviewService(product_id),getProductRecommendationService(product_id),getProductShoppingCartService(customer_id),getProductShippingService(product_id)])
    return JSONEncoder().encode(values)

def doTheMagic(product_id,customer_id):

    retval = asyncio.run(main(product_id,customer_id))

    return retval

