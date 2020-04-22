import requests
import json

data = ["ds", "34"]
r = requests.post("http://localhost:5000/sendData", data=json.dumps(data))