from flask import Flask, request
import Controller
from pymongo import MongoClient 
from flask import jsonify
import os
import json
from bson import ObjectId

app = Flask(__name__)

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


@app.route('/shopping_cart', methods=['POST'])
def index():

    cid=request.headers["Customer-Id"]
    res = Controller.retrieve_shopping_cart_by_customer_id(mongodbconnection,str(cid))

    if res:
        pass
    else:
        return jsonify(error=str({"message": "not found!"})), 404

    return json.dumps(JSONEncoder().encode(res))

#TODO Change port 
app.run(host="0.0.0.0", port=int("3000"), debug=True, threaded=True)
