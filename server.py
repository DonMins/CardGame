import json
import socket
import sys
import threading
import modell

BUFFER_SIZE = 2 ** 10
CLOSING = "Application closing..."
CONNECTION_ABORTED = "Connection aborted"
CONNECTED_PATTERN = "Client connected: {}:{}"
ERROR_ARGUMENTS = "Provide port number as the firstcommand line argument"
ERROR_OCCURRED = "Error Occurred"
EXIT = "exit"
JOIN_PATTERN = "{username} has joined"
RUNNING = "Server is running..."
SERVER = "SERVER"
SHUTDOWN_MESSAGE = "shutdown"
TYPE_EXIT = "Type 'exit' to exit>"
people = 1
WIN = "Вы победили!!!"
END_GAME = "покинул игру"


class Server(object):
    def __init__(self, argv):
        self.clients = set()
        self.countClients = 0
        self.listen_thread = None
        self.port = None
        self.sock = None
        self.message2 = None
        self.countCardUser1 = 14
        self.countCardUser2 = 14
        self.message1 = None


    def listen(self):
        self.sock.listen(1)  # become a server socket
        while True:
            try:
                client, address = self.sock.accept()  # accept connections from outside
            except OSError:
                print(CONNECTION_ABORTED)
                self.countClients = len(self.clients)
                return
            print(CONNECTED_PATTERN.format(*address))
            self.clients.add(client)  # добавили пользователя на один сервер
            self.countClients = len(self.clients)
            threading.Thread(target=self.handle, args=(client,)).start()  # начал работу поток

    def handle(self, client):
        while True:
            try:
                print(self.countClients)
                message = modell.Message(**json.loads(self.receive(client)))  # создали
                # объект класс и декодирование полученного сообщения
            except (ConnectionAbortedError, ConnectionResetError):
                self.countClients = len(self.clients)
                print(CONNECTION_ABORTED)
                return
            if message.quit:
                client.close()
                self.clients.remove(client)
                return

            mes = modell.Message(username=message.username, message=str(message.message), countClients = self.countClients)
            try:
                for client2 in self.clients:
                    if (client2 != client):
                        if (message.message == END_GAME):
                            mes = modell.Message(username=message.username, message=END_GAME, countClients=self.countClients)
                            self.senfFor(mes, client2)
                        else:
                            self.senfFor(mes, client2)
                    if (message.message == sys.maxsize):
                        if (client2 == client):
                            mes = modell.Message(username=message.username, message=str(sys.maxsize),countClients=self.countClients)
                            self.senfFor(mes, client2)
            except (ConnectionAbortedError, ConnectionResetError):
                self.countClients = len(self.clients)
                print(CONNECTION_ABORTED)

    def senfFor(self, message, client):
        client.sendall(message.marshal())

    def receive(self, client):  # считываение полученного сообщения
        buffer = ""
        while not buffer.endswith(modell.END_CHARACTER):
            buffer += client.recv(BUFFER_SIZE).decode(modell.TARGET_ENCODING)
            return buffer[:-1]

    def run(self):
        print(RUNNING)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # создание сокета
        self.sock.bind(("", 9091))  # привязать сокет к хосту и порту
        self.listen_thread = threading.Thread(target=self.listen)  # поток для прослушивания target - это
        # вызываемый объект, который вызывается методом run ()
        self.listen_thread.start()  # Начать активность потока.


    def exit(self):

        self.sock.close()

        for client in self.clients:
            client.close()

            print(CLOSING)
        self.countClients = len(self.clients)


if __name__ == "__main__":
    try:
        Server("9091").run()
    except RuntimeError as error:
        print(ERROR_OCCURRED)
        print(str(error))
