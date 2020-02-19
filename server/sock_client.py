class Sock_Client:

    def __init__(self, conn, addr):

        self.conn = conn
        self.addr = addr
        self.just_joined = True

    def set_name(self, name):
        self.name = name