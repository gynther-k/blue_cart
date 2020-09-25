import requests
import asyncio
from flask import jsonify,make_response
import json
from bson import ObjectId
import os
import time
import grpc
import Info_pb2
import Info_pb2_grpc


PRODUCT_INFO_SERVICE_ENDPOINT = os.environ['PRODUCT_INFO_SERVICE_SERVICE_SERVICE_HOST']+":50052"
#PRODUCT_INFO_SERVICE_ENDPOINT = "127.0.0.1:50051"

PRODUCT_RECOMMENDATION_SERVICE_ENDPOINT = os.environ['PRODUCT_RECOMMENDATION_SERVICE_SERVICE_HOST']+":50051"
#PRODUCT_RECOMMENDATION_SERVICE_ENDPOINT = "127.0.0.1:50052"

PRODUCT_REVIEW_SERVICE_ENDPOINT = os.environ['PRODUCT_REVIEW_SERVICE_SERVICE_HOST']+":50051"
#PRODUCT_REVIEW_SERVICE_ENDPOINT = "127.0.0.1:50053"

PRODUCT_SHIPPING_SERVICE_ENDPOINT = os.environ['PRODUCT_SHIPPING_SERVICE_SERVICE_HOST']+":50051"
#PRODUCT_SHIPPING_SERVICE_ENDPOINT = "127.0.0.1:50054"

PRODUCT_SHOPPING_CART_SERVICE_HOST = os.environ['PRODUCT_SHOPPING_CART_SERVICE_SERVICE_HOST']+":50051"
#PRODUCT_SHOPPING_CART_SERVICE_HOST = "127.0.0.1:50055"

class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)


async def getProductInfo(pid):
    #start_time = time.time()
    v={}    
    try:
        channel = grpc.insecure_channel(PRODUCT_INFO_SERVICE_ENDPOINT)

        stub = Info_pb2_grpc.InfoStub(channel)
        number = Info_pb2.Request(productid=str(pid))
        response = stub.GetInfo(number)
        
        for key in response.mapfield:
            v[key]=response.mapfield[key]
            
        v = json.dumps({"productInfo":json.loads(json.dumps(v))})
        v = json.loads(v)

    except IOError as err:
        print("IOError: {0}".format(err))
 
    return v

async def getProductReviewService(pid):

    v={}    
    try:
        channel = grpc.insecure_channel(PRODUCT_REVIEW_SERVICE_ENDPOINT)

        stub = Info_pb2_grpc.InfoStub(channel)
        number = Info_pb2.Request(productid=str(pid))
        response = stub.GetInfo(number)
        
        for key in response.mapfield:
            v[key]=response.mapfield[key]
            
        v = json.dumps({"Product_Review":json.loads(json.dumps(v))})
        v = json.loads(v)

    except IOError as err:
        print("IOError: {0}".format(err))
 
    return v

async def getProductRecommendationService(pid):

    v={}    
    try:
        channel = grpc.insecure_channel(PRODUCT_RECOMMENDATION_SERVICE_ENDPOINT)

        stub = Info_pb2_grpc.InfoStub(channel)
        number = Info_pb2.Request(productid=str(pid))
        response = stub.GetInfo(number)
        
        for key in response.mapfield:
            v[key]=response.mapfield[key]
            
        v = json.dumps({"Product_Recommendation":json.loads(json.dumps(v))})
        v = json.loads(v)

    except IOError as err:
        print("IOError: {0}".format(err))

    return v

async def getProductShoppingService(cid):

    v={}    
    try:
        channel = grpc.insecure_channel(PRODUCT_SHOPPING_CART_SERVICE_HOST)

        stub = Info_pb2_grpc.InfoStub(channel)
        number = Info_pb2.Request(productid=str(cid))
        response = stub.GetInfo(number)
        
        for key in response.mapfield:
            v[key]=response.mapfield[key]
            
        v = json.dumps({"Shopping_Cart":json.loads(json.dumps(v))})
        v = json.loads(v)

    except IOError as err:
        print("IOError: {0}".format(err))

    return v

async def getProductShippingService(pid):

    v={}    
    try:
        #print("start getProductShipping")
        channel = grpc.insecure_channel(PRODUCT_SHIPPING_SERVICE_ENDPOINT)

        stub = Info_pb2_grpc.InfoStub(channel)
        number = Info_pb2.Request(productid=str(pid))
        response = stub.GetInfo(number)
        
        for key in response.mapfield:
            v[key]=response.mapfield[key]
            
        v = json.dumps({"Shipping":json.loads(json.dumps(v))})
        v = json.loads(v)

    except IOError as err:
        print("IOError: {0}".format(err))

    return v






async def main(product_id,customer_id):
    values = await asyncio.gather(*[getProductInfo(product_id),getProductReviewService(product_id),getProductRecommendationService(product_id),getProductShoppingService(customer_id),getProductShippingService(product_id)])
    return JSONEncoder().encode(values)

def doTheMagic(product_id,customer_id):

    retval = asyncio.run(main(product_id,customer_id))

    return retval

