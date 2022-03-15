import websocket
import time
import hashlib
import hmac
import base64
import json

def hmac_header(secret, message=None):
    hash = hmac.new(secret, msg=message, digestmod=hashlib.sha256)

    # to lowercase hexits
    hash.hexdigest()

    # to base64
    return base64.b64encode(hash.digest())

def generate_header():
    api_key = ""
    secret_key = bytes("", "utf-8")
    timestamp = str(int(round(time.time() * 1000)))
    timewindow = "20000"

    message = api_key + timestamp + timewindow
    signature = hmac_header(secret_key, bytes(message, 'utf-8'))
    return {
            'dv-api-key': api_key,
            'dv-timestamp': timestamp,
            'dv-timewindow': timewindow,
            'dv-signature': signature.decode('utf-8'),
           }

def send_dummy_message():
    ws = websocket.WebSocket()
    header = generate_header()
    ws.connect("wss://sandbox.trade.dvchain.co/websocket", header=header)
    
    message = {
    'type': 'subscribe',
    'topic': 'BTC/USD',
    'event': "levels",
    'data': {}
    }

    ws.send(json.dumps(message))
    time.sleep(1)
    print(ws.recv())
        
    ws.close()

if name == "main":
    send_dummy_message()
