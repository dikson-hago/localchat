#!/usr/bin/env python3
from twisted.internet.protocol import Protocol, Factory
from twisted.internet import reactor
from random import randint

class Client(Protocol):
    ip: str = None
    login: str = None
    factory: 'Chat'


    def __init__(self, factory):
        self.factory = factory

    def connectionMade(self):
        self.ip = self.transport.getPeer().host
        self.factory.counter_clients = self.factory.counter_clients + 1
        print(f"client connected {self.ip}\n")
        #self.transport.write("welcome to chat\n".encode())
        if self.factory.counter_clients != 1:
            #self.transport.write("your contacts are: \n".encode())
            counter = 1
            for user in self.factory.clients:
                if counter < self.factory.counter_clients:
                    self.transport.write(f"contact:{user.login}\n".encode())
                counter = counter + 1
    def dataReceived(self, data: bytes):
        message = data.decode().replace('\n', '')
        print(message)
        if self.login is not None:
            getter_login = ''
            getter_message = ''
            counter_slashes = 0
            for i in range(0, len(message)):
                if message[i] == ':' and counter_slashes == 0:
                    counter_slashes = counter_slashes + 1
                    getter_login = getter_message
                    getter_message = ''
                else:
                    getter_message = getter_message + message[i]
            my_login = self.login
            my_login.replace("\r", "")
            print(f"{my_login} >> {getter_login}\n")

            self.factory.notify_one_user(getter_message, getter_login)
        else:
            if message.startswith("login:"):
                self.login = message.replace("login:", "")
                self.factory.clients.append(self)
                notification = f"contact:{self.login}"
                self.factory.notify_all_users(notification)
                print(notification, "\n")
            else:
                print("error: invalid client login\n")

    def connectionLost(self, reason=None):
        self.factory.clients.remove(self)
        print(f"client disconnected: {self.ip} \n")

class Chat(Factory):
    clients: list
    counter_clients: int

    def __init__(self):
        self.clients = []
        self.counter_clients = 0

    def startFactory(self):
        print("server started\n")

    def buildProtocol(self, addr):
        return Client(self)

    def notify_all_users(self, data: str):
        for user in self.clients:
            user.transport.write((data + '\n').encode())

    def notify_one_user(self, data: str, username: str):
        for user in self.clients:
            if user.login == username + '\r':
                user.transport.write((data + '\n').encode())



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    reactor.listenTCP(7410, Chat())
    reactor.run()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
