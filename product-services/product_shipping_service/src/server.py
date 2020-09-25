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
#uri = "mongodb+srv://gynther:admin@cluster0.ypo7l.azure.mongodb.net/products?retryWrites=true&w=majority"
conn='null'
mongodbconnection='null'
PORT='[::]:50051' 
#PORT='[::]:50054'

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
        
        res = Controller.retrieve_shipping()

        if res:
            pass
        else:
            return str({"message": "not found!"})
                
        response.mapfield["shipping"]=str(res)
        #print("response")
        #print(res)

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