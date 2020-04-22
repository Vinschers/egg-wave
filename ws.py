import os
from flask import Flask, jsonify, request, render_template, Response, send_file, stream_with_context, make_response
import json
import numpy as np
import pandas as pd

app = Flask(__name__)

@app.route("/")
def index():
    return "<h1>EGG WAVE - FUNCIONANDO</h1>"

@app.route("/sendData", methods=['GET', 'POST'])
def sendData():
    info = request.data
    info = json.loads(info)
    print(info)
    return "200"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, threaded=True)