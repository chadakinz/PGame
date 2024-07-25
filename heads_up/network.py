from socket import *
import dill as pickle
class Network:
    def __init__(self, purpose):
        self.client = socket(AF_INET, SOCK_STREAM)
        self.server = "192.168.1.7"
        self.port = 5556
        self.addr = (self.server, self.port)
        self.id  = self.connect()
        #print(self.id)
        self.purpose = self.send(purpose)

    def connect(self):
        try:
            self.client.connect(self.addr)
        except:

            print('Error connecting')



    def send(self, data):
        try:
            #self.client.connect(self.addr)

            self.client.send(pickle.dumps(data))

            x = pickle.loads(self.client.recv(2048))

            return x
        except error as e:
            print(e)

    def receive(self):
        print(f'waiting for info')
        x = pickle.loads(self.client.recv(2048))

        return x


