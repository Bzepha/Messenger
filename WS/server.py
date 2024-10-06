import asyncio
import json
from websockets.asyncio.server import serve
from client import client

clients = {}

async def handler(websocket):
    async for message in websocket:
        message = json.loads(message)
        if message['Type'] == 'ECHO':
            await websocket.send(message['Message'])
        elif message['Type'] == 'SEND':
            recipient = clients.get(message['Recipient'])
            recipient.add_message(message['Sender'], message['Message'])
            sender = clients.get(message['Sender'])
            sender.add_self_message(message['Recipient'], message['Message'])
        elif message['Type'] == 'LOGIN':
            if clients.get(message['Sender']) == None:
                clients[message['Sender']] = client(message['Sender'], {})
            await websocket.send('Welcome in ' + message['Sender'])
        elif message['Type'] ==  'GET':
            await websocket.send(clients.get(message['Sender']).get_chat_history(message['Recipient']))
        elif message['Type'] == 'STOP':
            open('save.json', 'w').close()
            file = open('save.json', 'a')
            file.write('{')
            for users in clients:
                file.write('"' + users + '"' + ':')
                file.write(clients[users].save())
                file.write(',')
            file.write('"SAVE": "DONE"}')
            file.close()
            exit()
        else:
            await websocket.send('Message Type not compatible')

async def main():
    async with serve(handler, 'localhost', 80):
        print('Starting')
        await asyncio.get_running_loop().create_future()

def start():
    with open('save.json') as read:
        try: 
            save = json.load(read)
            for saves in save:
                if save[saves] == "DONE":
                    break
                else:
                    clients[saves] = client(save[saves][saves], save[saves][saves]['MESSAGEHISTORY'])
        finally: 
            asyncio.run(main())