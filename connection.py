class Connection:

    def __init__(self, client, addr):

        self.client = client
        self.addr = addr

    def set_name(self, name):
        self.name = name

        # self.name = name