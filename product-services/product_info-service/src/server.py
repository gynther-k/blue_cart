import grpc
from concurrent import futures
import time
import json
from pymongo import MongoClient 
import os

# import the generated classes
import Info_pb2
import Info_pb2_grpc

# import the original Controller.py
import Controller

uri = "mongodb+srv://"+os.environ['MONGO_DB_USERNAME']+":"+os.environ['MONGO_DB_PASSWORD']+"@"+os.environ['MONGO_DB_CLUSTER_ADDRESS']+"?retryWrites=true&w=majority"
conn='null'
mongodbconnection='null'
PORT='[::]:50052' 
#PORT='[::]:50051'

try: 
    conn = MongoClient(uri)
    mongodbconnection = conn.products #database name
except Exception as err:
    print("Exception in mongoDB: {0}".format(err))

#classname From bottom of proto file
class InfoServicer(Info_pb2_grpc.InfoServicer):

    # rpc GetProductInfo from proto
    def GetInfo(self, request, context):
        response = Info_pb2.Reply()
        
        res = Controller.retrieve_Product_By_Id(mongodbconnection,request.productid)

        if res:
            pass
        else:
            return str({"message": "not found!"})      
        
        response.mapfield["productid"]=res['product_id']
        response.mapfield["productname"]=res['product_name']
        response.mapfield["shortdescription"]=res['short_description']
        response.mapfield["longdescription"]=res['long_description']
        response.mapfield["price"]=str(res['price'])
        response.mapfield["currency"]=res['currency']
        response.mapfield["productcategory"]=res['product_category']
        response.mapfield["productimage"]=res['product_image']

        return response


# create a gRPC server
server = grpc.server(futures.ThreadPoolExecutor())

# use the generated function
# to add the defined class to the server
Info_pb2_grpc.add_InfoServicer_to_server(
        InfoServicer(), server)

print('Starting server. Listening on port: '+PORT)
server.add_insecure_port(PORT)
server.start()

# since server.start() will not block,
# a sleep-loop is added to keep alive
try:
    while True:
        time.sleep(86400)
except KeyboardInterrupt:
    server.stop(0)

#python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. Info.proto