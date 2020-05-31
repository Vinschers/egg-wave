import os
from flask import Flask, jsonify, request, render_template, Response, send_file, stream_with_context, make_response
import json
import numpy as np
import pandas as pd
from flask_cros import CORS

app = Flask(__name__)
CORS(app)
cors = CORS(app, resources={
    r"/*":{
        "origins":"*"
    }
})

data = {}

@app.route("/")
def index():
    return "<h1>EGG WAVE - FUNCIONANDO</h1>"

@app.route("/sendData", methods=['POST'])
def sendData():
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





@app.route("/submit", methods=['POST'])
def submit():
    density = request.form['density']
    air = request.form['air']
    icu = request.form['icu']
    isolation = request.form['isolation']

    # chamar algoritmo pedro
    return "teste submit" # retorna json pro site 
    
@app.route('/country/<name>', methods=['GET'])
def country(name):
    df = pd.read_csv('final.csv')
    df.set_index('Name', inplace=True)
    df.drop(df.columns[0], axis=1, inplace=True)
    return df.loc[name].to_json()







if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, threaded=True)