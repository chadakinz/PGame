from socket import *
import pickle
class Network:
    def __init__(self):
        self.client = socket(AF_INET, SOCK_STREAM)
        self.server = "192.168.1.200"
        self.port = 5555
        self.addr = (self.server, self.port)
        self.id  = self.connect()
        #print(self.id)

    def connect(self):
        try:
            self.client.connect(self.addr)

            return pickle.loads(self.client.recv(2048))
        except:
            print('2')



    def send(self, data):
        try:
            #self.client.connect(self.addr)

            self.client.send(pickle.dumps(data))

            x = pickle.loads(self.client.recv(2048))

            return x
        except error as e:
            print(e)




