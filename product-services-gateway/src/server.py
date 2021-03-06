from flask import Flask, request
import Controller
from flask import jsonify,make_response
import json
from bson import ObjectId
import time
# from waitress import serve

app = Flask(__name__)

class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)


@app.route('/product_service_proxy', methods=['GET'])
def post_route():

    start_time = time.time()
    product_id=request.headers["Product-Id"]
    customer_id=request.headers["Customer-Id"]

    result=Controller.doTheMagic(product_id,customer_id)
  
    if result:
        result=json.dumps({"result":json.loads(result),"duration":((time.time() - start_time)*1000)}) 
        result=json.loads(result)
        result=JSONEncoder().encode(result)
    else:
        print("fail")
        return jsonify(error=str({"message": "not found!"})), 404

    return make_response(result,200)


#TODO Change port 
app.run(host="0.0.0.0", port=int("3000"), debug=True, threaded=True, processes=1)
# serve(app, host="0.0.0.0", threads=32, port=3000)