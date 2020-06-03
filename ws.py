import os
from flask import Flask, jsonify, request, render_template, Response, send_file, stream_with_context, make_response
import json
import numpy as np
import pandas as pd
from ML import categorizador

app = Flask(__name__)

from Hackathon import hackathon
hackathon.inialize()
hackathon.routes(app)

data = {}

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/sendData", methods=['POST'])
def sendData():
    print(info)
    info = request.data
    info = json.loads(info)
    ipv4 = request.remote_addr

    if not ipv4 in data:
        data[ipv4] = []

    data[ipv4].append(info)

    return "200"

@app.route("/getData", methods=['GET'])
def getData():
    ipv4 = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)   

    ret = {"ipv4": ipv4, "data": data[ipv4] if ipv4 in data else None}

    return json.dumps(ret)

@app.route('/sendFile', methods=['POST'])
def sendFile():
    file = request.files['file']
    return jsonify(categorizador.categoriza(file))


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, threaded=True)