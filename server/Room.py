class Room:

    def __init__(self, name, password):

        self.name = name
        self.password = password

        self.clients = []
        self.messages = []

    def add_client(self, client):
        self.clients.append(client)

    def remove_client(self, client):
        self.clients.remove(client)

    def add_message(self, message):
        self.messages.append(message)