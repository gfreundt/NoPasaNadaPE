import requests, json
from pprint import pprint

url = "http://192.168.68.105:5000/update"
_post = {"token": "token", "instruction": "get_records_to_update"}

f = requests.post(url, json=_post)
print(f.status_code)
x = f.json()

print(x)
