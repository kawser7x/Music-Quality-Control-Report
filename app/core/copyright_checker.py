# core/copyright_checker.py

import requests
import hashlib
import hmac
import time
import base64

AUDD_API_TOKEN = "2aa858d23ee0b0b045efc766ccc3e936"

ACR_HOST = "https://identify-ap-southeast-1.acrcloud.com/v1/identify"
ACR_ACCESS_KEY = "9cbcc2200d3740234b864010d4e6bced"
ACR_ACCESS_SECRET = "MdAatKjm9nI0B33YWGofP5AKFt4ZESGgsFLEtNqx"

def check_audd(file_path: str) -> dict:
    with open(file_path, 'rb') as f:
        files = {
            'file': f,
        }
        data = {
            'api_token': AUDD_API_TOKEN,
            'return': 'timecode,apple_music,deezer,spotify',
        }
        response = requests.post('https://api.audd.io/', data=data, files=files)
        return response.json()

def check_acrcloud(file_path: str) -> dict:
    http_method = "POST"
    http_uri = "/v1/identify"
    data_type = "audio"
    signature_version = "1"
    timestamp = str(int(time.time()))

    string_to_sign = f"{http_method}\n{http_uri}\n{ACR_ACCESS_KEY}\n{data_type}\n{signature_version}\n{timestamp}"
    sign = base64.b64encode(
        hmac.new(ACR_ACCESS_SECRET.encode(), string_to_sign.encode(), hashlib.sha1).digest()
    ).decode()

    files = {'sample': open(file_path, 'rb')}
    data = {
        'access_key': ACR_ACCESS_KEY,
        'data_type': data_type,
        'signature_version': signature_version,
        'signature': sign,
        'timestamp': timestamp,
    }

    response = requests.post(ACR_HOST, files=files, data=data)
    return response.json()

def run_copyright_checks(file_path: str) -> dict:
    audd_result = check_audd(file_path)
    acr_result = check_acrcloud(file_path)

    return {
        "audd": audd_result,
        "acrcloud": acr_result
    }