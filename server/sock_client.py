class Sock_Client:

    def __init__(self, conn, addr):

        self.conn = conn
        self.addr = addr

    def set_name(self, name):
        self.name = name