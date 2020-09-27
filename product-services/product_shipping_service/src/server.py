from flask import Flask, request
import Controller
from flask import jsonify
import os
import json
from bson import ObjectId
from waitress import serve

app = Flask(__name__)

class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)


@app.route('/shipping', methods=['GET'])
def index():
    #pid=request.headers["Product-Id"]
    res = Controller.retrieve_shipping()

    if res:
        pass
    else:
        return jsonify(error=str({"message": "not found!"})), 404

    return json.dumps(JSONEncoder().encode(res))

#app.run(host="0.0.0.0", port=int("3000"), debug=True, threaded=True)
serve(app, host="0.0.0.0", threads=32, port=3000)