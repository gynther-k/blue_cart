import requests
import asyncio
from flask import jsonify,make_response
import json
from bson import ObjectId
import os
import time

PRODUCT_INFO_SERVICE_ENDPOINT = "http://"+os.environ['PRODUCT_INFO_SERVICE_SERVICE_SERVICE_HOST']+"/product"
#PRODUCT_INFO_SERVICE_ENDPOINT = "http://"+"127.0.0.1:3001"+"/product"

PRODUCT_RECOMMENDATION_SERVICE_ENDPOINT = "http://"+os.environ['PRODUCT_RECOMMENDATION_SERVICE_SERVICE_HOST']+"/recommendation"
#PRODUCT_RECOMMENDATION_SERVICE_ENDPOINT = "http://"+"127.0.0.1:3004"+"/recommendation"

PRODUCT_REVIEW_SERVICE_ENDPOINT = "http://"+os.environ['PRODUCT_REVIEW_SERVICE_SERVICE_HOST']+"/review"
#PRODUCT_REVIEW_SERVICE_ENDPOINT = "http://"+"127.0.0.1:3003"+"/review"

PRODUCT_SHIPPING_SERVICE_ENDPOINT = "http://"+os.environ['PRODUCT_SHIPPING_SERVICE_SERVICE_HOST']+"/shipping"
#PRODUCT_SHIPPING_SERVICE_ENDPOINT = "http://"+"127.0.0.1:3002"+"/shipping"

PRODUCT_SHOPPING_CART_SERVICE_HOST = "http://"+os.environ['PRODUCT_SHOPPING_CART_SERVICE_SERVICE_HOST']+"/shopping_cart"
#PRODUCT_SHOPPING_CART_SERVICE_HOST = "http://"+"127.0.0.1:3005"+"/shopping_cart"


class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)


async def getProductInfo(pid):
        
    try:
        v = requests.post(PRODUCT_INFO_SERVICE_ENDPOINT, headers = {"product_id" : str(pid)})
        v = json.dumps({"productInfo":json.loads(v.json())})
        v = json.loads(v)

    except IOError as err:
        print("IOError: {0}".format(err))
 
    return v

async def getProductReviewService(pid):
        
    try:
        v = requests.post(PRODUCT_REVIEW_SERVICE_ENDPOINT, headers = {"product_id" : str(pid)})
        v = json.dumps({"Product_Review":json.loads(v.json())})
        v = json.loads(v)

    except IOError as err:
        print("IOError: {0}".format(err))
 
    return v

async def getProductRecommendationService(pid):
        
    try:
        v = requests.post(PRODUCT_RECOMMENDATION_SERVICE_ENDPOINT, headers = {"product_id" : str(pid)})
        v = json.dumps({"Recommendation_List":json.loads(v.json())})
        v = json.loads(v)

    except IOError as err:
        print("IOError: {0}".format(err))
 
    return v

async def getProductShippingService(pid):
        
    try:
        v = requests.post(PRODUCT_SHIPPING_SERVICE_ENDPOINT)
        v = json.dumps({"Product_Shipping":json.loads(v.json())})
        v = json.loads(v)

    except IOError as err:
        print("IOError: {0}".format(err))
 
    return v


async def getProductShoppingCartService(cid):
        
    try:
        v = requests.post(PRODUCT_SHOPPING_CART_SERVICE_HOST, headers = {"customer_id" : str(cid)})
        v = json.dumps({"Shopping_Cart":json.loads(v.json())})
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

