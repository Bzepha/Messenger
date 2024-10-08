import json

class client:

    name = None
    chats = {} # chating with : (Who sent, message)

    def get_chat_history(self, request):
        return json.dumps({'Message': self.chats.get(request, None)})

    def add_message(self, sender, message):
        if self.chats.get(sender) == None:
            self.chats[sender] = []
        self.chats.get(sender).append(str(sender) + ': ' + str(message))
        return        
    
    def add_self_message(self, recipient, message):
        if self.chats.get(recipient) == None:
            self.chats[recipient] = []
        self.chats.get(recipient).append(str(self.name) + ': ' + str(message))
        return   

    def save(self):
        return json.dumps({self.name: {'MESSAGEHISTORY': self.chats}})

    def __hash__(self) -> int:
        return hash(self.name)
    
    def __str__(self) -> str:
        return self.name

    def __init__(self, name, chat) -> None:
        self.name = name
        self.chats = chat
