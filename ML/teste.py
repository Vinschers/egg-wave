import requests
import json

data = "sdfsfsfsdf"
r = requests.post("http://localhost:5000/sendData", data=json.dumps(data))