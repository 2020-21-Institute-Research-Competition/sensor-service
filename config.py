import requests
import json
import multiprocessing


def _prepare_request(token, data):
    url = 'http://192.168.43.142:8080'
    payload = json.dumps(data)
    headers = {'Content-Type': 'application/json'}
    requests.post(f'{url}/api/v1/{token}/telemetry', headers=headers, data=payload)
    
def post(token, data):
    proc = multiprocessing.Process(target=_prepare_request, args=(token, data))
    proc.start()
    
