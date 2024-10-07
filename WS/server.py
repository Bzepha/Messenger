import asyncio
import json
from websockets.asyncio.server import serve
from client import client

# Holds all of the clients that have logged in with their username as the key
clients = {}

async def handler(websocket):
    async for message in websocket:
        # Loads message from a JSON format
        message = json.loads(message)
        # Refer to ECHO in docs.txt
        if message['Type'] == 'ECHO':
            # Websocket sends back what was given in the 'Message' section
            await websocket.send(message['Message'])
        # Reference in SEND of docs.txt
        elif message['Type'] == 'SEND':
            # Grabs the recipient from the clients dictionary
            recipient = clients.get(message['Recipient'])
            # Adds the message to the 'chats' section of the client
            recipient.add_message(message['Sender'], message['Message'])
            # Next two lines does the same as the recipient but for the Sender.
            sender = clients.get(message['Sender'])
            sender.add_self_message(message['Recipient'], message['Message'])
        # Reference in LOGIN of docs.txt
        elif message['Type'] == 'LOGIN':
            # Checks if client is already in 'clients'. If they aren't a new user is added
            if clients.get(message['Sender']) == None:
                clients[message['Sender']] = client(message['Sender'], {})
            # Sends back a welcome in message.
            await websocket.send('Welcome in ' + message['Sender'])
        # Reference in GET of docs.txt
        elif message['Type'] ==  'GET':
            # Sends the websocket a users conversation with another
            await websocket.send(clients.get(message['Sender']).get_chat_history(message['Recipient']))
        # Reference in STOP of docs.txt
        elif message['Type'] == 'STOP':
            # Opens file that get saved
            open('save.json', 'w').close()
            # Deletes old save data
            file = open('save.json', 'a')
            # Writes to the save file
            file.write('{')
            for users in clients:
                file.write('"' + users + '"' + ':')
                file.write(clients[users].save())
                file.write(',')
            file.write('"SAVE": "DONE"}')
            # Closes the file
            file.close()
            # Force exits the program
            exit()
        else:
            await websocket.send('Message Type not compatible')

async def main():
    # Starts the server on localhost on port 80
    async with serve(handler, 'localhost', 80):
        print('Starting')
        await asyncio.get_running_loop().create_future() # Runs Forever

# Call this when you want to run the program
def start():
    # Opens the save file and writes the data to the 'clients' dictionary
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