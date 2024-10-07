import json
from websockets.sync.client import connect

with connect('ws://localhost:80') as websocket:
    websocket.send(json.dumps({'Type': 'STOP'}))