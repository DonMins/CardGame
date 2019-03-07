import json
import socket
import threading
import messagess
import modell
import views

BUFFER_SIZE = 2 ** 10

class Application(object):
    instance = None

    def __init__(self, args):
        self.args = args
        self.closing = False
        self.host = None
        self.port = None
        self.receive_worker = None
        self.sock = None
        self.username = None
        self.ui = views.EzChatUI(self)
        self.allCard=14 # максимальное число карт в колоде
        self.count=0
        self.countOut=0
        self.countInHead=4# число карт в руках
        self.lastUser = None
        Application.instance = self

    def getCountOut(self):
        return self.countOut

    def getAllcard(self):
        return self.allCard

    def execute(self):
        if not self.ui.show():# появление формы
            return
        self.sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM) # создали сокет
        try:
            self.sock.connect(('localhost', 9090))# пытаемся подрубиться к серваку
        except (socket.error, OverflowError):
            self.ui.alert(messagess.ERROR, messagess.CONNECTION_ERROR)# ошибка если сервак не врублен
            return

        self.receive_worker =threading.Thread(target=self.receive)
        self.receive_worker.start()
        self.ui.loop()

    def receive(self):
        while True:
            try:
                message =modell.Message(**json.loads(self.receive_all()))
                print(str(message.message))
                self.countOut = int(message.message)
                self.allCard = self.allCard + int(message.message)
                if (self.allCard>=0):
                    mes = modell.Message(username="Бог Судья ",
                                     message= " Ирок  " + message.username + " отобрал у вас  " + str(message.message)
                                              +" карты " + " [Баланс = " + str(self.allCard) + " ]")
                else:
                    mes = modell.Message(username="Бог Судья ",
                                         message=" Ирок  " + message.username + " Победил")

            except (ConnectionAbortedError, ConnectionResetError):
                if not self.closing:
                    self.ui.alert(messagess.ERROR, messagess.CONNECTION_ERROR)
                return
            self.ui.show_message(mes)


    def receive_all(self):
        buffer = ""
        while not buffer.endswith(modell.END_CHARACTER):
            buffer +=self.sock.recv(BUFFER_SIZE).decode(modell.TARGET_ENCODING)
        return buffer[:-1]


    def send(self, event=None):

        message = self.ui.message.get()
        self.ui.message.set("")
        message = modell.Message(username=self.username, message=message, count=self.count, quit=False)
        self.ui.forth_button['state'] = views.TEXT_STATE_DISABLED
        self.ui.third_button['state'] = views.TEXT_STATE_DISABLED
        self.ui.second_button['state'] = views.TEXT_STATE_DISABLED
        self.ui.first_button['state'] = views.TEXT_STATE_DISABLED

        try:
            self.sock.sendall(message.marshal())
        except (ConnectionAbortedError,ConnectionResetError):
            if not self.closing:
                self.ui.alert(messagess.ERROR, messagess.CONNECTION_ERROR)

    def exit(self):
        self.closing = True
        try:
            self.sock.sendall(modell.Message(username=self.username, message="", quit=True).marshal())
        except (ConnectionResetError,ConnectionAbortedError, OSError):
            print(messagess.CONNECTION_ERROR)
        finally:
            self.sock.close()




