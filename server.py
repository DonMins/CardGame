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


class Server(object):

    def __init__(self, argv):
        self.clients = set()
        self.listen_thread = None
        self.port = None
        self.sock = None
        self.message2 = None
        self.count2 = 10
        self.message1 = None
        self.count1 = 10
        self.parse_args(argv)
        self.people = 1

    def listen(self):
        self.sock.listen(1)#become a server socket
        while True:
            try:
                client, address = self.sock.accept() #accept connections from outside

            except OSError:
                print(CONNECTION_ABORTED)
                return
            print(CONNECTED_PATTERN.format(*address))
            self.clients.add(client) # добавили пользователя на один сервер
            threading.Thread(target=self.handle,args=(client,)).start()# начал работу поток

    def handle(self, client):
        while True:
            try:
                message = modell.Message(**json.loads(self.receive(client))) # создали
                print(message.message)

                # объект класс и декодирование полученного сообщения
            except (ConnectionAbortedError, ConnectionResetError):
                print(CONNECTION_ABORTED)
                return
            if message.quit:
                client.close()
                self.clients.remove(client)
                return

            if SHUTDOWN_MESSAGE.lower() == message.message.lower():
                self.exit()
                return

            if self.people==1:
                self.message1=message


            if self.people==2:
                self.message2=message

            self.people += 1

            if self.people == 3:
                if (self.message1.username == 'Don'):
                    self.count2 =self.count2+int(self.message1.message)
                if (self.message2.username == 'Tany'):
                    self.count1 = self.count1 + int(self.message2.message)


                mes = modell.Message(username="System",
                                     message="Карт у :" + self.message1.username + "  осталось " + str(self.count1)+ " y "+
                                             self.message2.username + "  осталось " + str(self.count2))
                self.broadcast(mes)
                self.people = 1







    def broadcast(self, message):
        for client in self.clients:
            client.sendall(message.marshal())


    def receive(self, client):                    # считываение полученного сообщения
        buffer = ""
        while not buffer.endswith(modell.END_CHARACTER):
            buffer +=client.recv(BUFFER_SIZE).decode(modell.TARGET_ENCODING)
            return buffer[:-1]

    def run(self):
        print(RUNNING)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #создание сокета
        self.sock.bind(("", 9090)) # привязать сокет к хосту и порту
        self.listen_thread =threading.Thread(target=self.listen)# поток для прослушивания target - это
        # вызываемый объект, который вызывается методом run ()
        self.listen_thread.start()#Начать активность потока.

    def parse_args(self, argv):
        if len(argv) != 4:
            raise RuntimeError(ERROR_ARGUMENTS)
        try:
            self.port = int(argv[1])
        except ValueError:
            raise RuntimeError(ERROR_ARGUMENTS)


    def exit(self):
        self.sock.close()
        for client in self.clients:
            client.close()
            print(CLOSING)

if __name__ == "__main__":
    try:
        Server("9090").run()
    except RuntimeError as error:
        print(ERROR_OCCURRED)
        print(str(error))
