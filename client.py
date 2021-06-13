from twisted.internet import stdio, reactor
from twisted.internet.protocol import ClientFactory, Protocol

class DataWrapper(Protocol):
    output = None

    def dataReceived(self, data: bytes):
        if data.decode() == 'exit\n':
            reactor.callFromThread(reactor.stop)

        if self.output:
            self.output.write(data)

class UserProtocol(DataWrapper):
    def wrap_input(self):
        input_forwarder = DataWrapper()
        input_forwarder.output = self.transport

        stdio_wrapper = stdio.StandardIO(input_forwarder)
        self.output = stdio_wrapper

    def connectionMade(self):
        print("connection ok")
        self.transport.write(f"login:{self.factory.login}".encode())
        self.wrap_input()

class UserFactory(ClientFactory):
    protocol = UserProtocol
    login: str

    def __init__(self, user_login: str):
        self.login = user_login

    def startedConnecting(self, connector):
        print("connecting to the server\n")

    def clientConnectionLost(self, connector, reason):
        print("disconnected\n")
        reactor.callFromThread(reactor.stop)

    def clientConnectionFailed(self, connector, reason):
        print("connection failed\n")
        reactor.callFromThread(reactor.stop)

if __name__ == '__main__':
    login = input("Your login >>")
    reactor.connectTCP(
        "localhost",
        7410,
        UserFactory(login)
    )
    reactor.run()