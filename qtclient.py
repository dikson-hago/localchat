#!/usr/bin/env python3
import sys
from PyQt5 import QtWidgets
import design
import crypto
from twisted.internet import stdio
from random import randint
from twisted.internet.protocol import ClientFactory, Protocol
from twisted.protocols.basic import LineOnlyReceiver

class ChatClient(LineOnlyReceiver):
    factory: 'ChatFactory'
    contacts: list
    counter_contacts: int

    def __init__(self, factory):
        self.factory = factory
        self.contacts = []
        self.counter_contacts = 0

    def connectionMade(self):
        self.factory.window.protocol = self

    def lineReceived(self, line):
        message = line.decode()
        if message.startswith("contact:"): #add new contact
            self.contacts.append(message)
            self.counter_contacts = self.counter_contacts + 1
            self.factory.window.ContactsEdit.appendPlainText(message)
        else:
            self.factory.window.plainTextEdit.appendPlainText(message)

class ChatFactory(ClientFactory):

    window: 'ExampleApp'

    def __init__(self, window):
        self.window = window

    def buildProtocol(self, addr):
        return ChatClient(self)

class ExampleApp(QtWidgets.QMainWindow, design.Ui_MainWindow):

    protocol: ChatClient
    reactor = None
    login = ''

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.init_handlers()

    def init_handlers(self):
        self.SendButton.clicked.connect(self.send_message)

    def closeEvent(self, event):
        self.reactor.callFromThread(self.reactor.stop)

    def send_message(self):
        message = self.lineEdit.text()
        getter_login = ''
        getter_message = ''
        counter_slashes = 0
        for i in range(0, len(message)):
            if message[i] == ':':
                counter_slashes = counter_slashes + 1
                if counter_slashes == 1:
                    getter_login = getter_message
                    getter_message = ''
            else:
                getter_message = getter_message + message[i]
        if message.startswith("login:"):
            self.login = getter_message
        else:
            message = getter_login + ':' + self.login + ':' + getter_message
        self.protocol.sendLine(message.encode())
        self.lineEdit.setText('')

def main():
    app = QtWidgets.QApplication(sys.argv)
    import qt5reactor

    window = ExampleApp()
    window.show()

    qt5reactor.install()

    from twisted.internet import reactor

    reactor.connectTCP(
        "localhost",
        7410,
        ChatFactory(window)
    )

    window.reactor = reactor
    reactor.run()

    #app.exec_()

if __name__ == '__main__':
    main()