import json
import socket
import threading
import messagess
import sys
import modell
import views

BUFFER_SIZE = 2 ** 10


class Application(object):

    def __init__(self):
        self.closing = False
        self.host = None
        self.port = None
        self.receive_worker = None
        self.sock = None
        self.username = None
        self.ui = views.EzChatUI(self)
        self.allCard = 14  # максимальное число карт в колоде
        self.cardRival = 15 # карты противника
        self.countOut = 0
        self.startcard = 0
        self.winner = False
        self.loser = False
        self.countClients = 1

    def getCountOut(self):
        return self.countOut

    def getAllcard(self):
        return self.allCard

    def execute(self):
        if not self.ui.show():  # появление формы
            return
        self.sock = socket.socket()  # создали сокет
        try:
            self.sock.connect(('localhost', 9092))  # пытаемся подрубиться к серваку\

        except (socket.error, OverflowError):
            self.ui.alert(messagess.ERROR, messagess.CONNECTION_ERROR)  # ошибка если сервак не врублен
            return

        self.receive_worker = threading.Thread(target=self.receive)
        self.receive_worker.start()
        self.ui.loop()

    def receive(self):
        while True:
            try:
                message = modell.Message(**json.loads(self.receive_all()))
                self.countClients = int(message.countClients)
                self.startcard = int(message.startcard)

                if ((message.message) == messagess.END_GAME):
                    mes = modell.Message(username="Бог Судья ",
                                         message="Второй игрок покинул игру(( Вы Победили!!!")
                    self.winner = True
                    self.ui.show_message_final2(mes)
                    self.ui.repeat_button.pack_forget()
                    return

                if (int(message.message) == sys.maxsize):
                    mes = modell.Message(username="Бог Судья ",
                                         message="Победа!!!")
                    self.winner = True
                    self.ui.show_message_final(mes)

                    return
                if (int(message.message)<1):
                    self.countOut = int(message.message)

                self.allCard = self.allCard + self.countOut  # мой баланс

                if (self.allCard > 1 and self.cardRival > 0 and int(message.message)<1):
                    mes = modell.Message(username="Бог Судья ",
                                         message=" Ирок  " + message.username + " отобрал у вас  " + str(
                                             message.message)
                                                 + " карты " + " [Ваш баланс = " + str(self.allCard) + " ]  " +
                                                 "[ Баланс противника = " + str(self.cardRival) + " ]")
                elif(self.startcard !=2 and int(message.message)<1):

                    self.loser = True
                    mes = modell.Message(username="Бог Судья ",
                                         message=" Ирок  " + message.username + " Победил")
                    messag = str(sys.maxsize)
                    message = modell.Message(username=self.username, message=messag, quit=False)
                    try:
                        self.sock.sendall(message.marshal())

                    except (ConnectionAbortedError, ConnectionResetError):
                        if not self.closing:
                            self.ui.alert(messagess.ERROR, messagess.CONNECTION_ERROR)
                elif(self.countClients==1):
                    mes = modell.Message(username="Бог Судья ",
                                         message=" Ждём")
                else:
                    mes = modell.Message(username="Бог Судья ",
                                         message=" Играем")

            except (ConnectionAbortedError, ConnectionResetError):
                if not self.closing:
                    self.ui.alert(messagess.ERROR, messagess.CONNECTION_ERROR)
                return
            self.ui.show_message(mes)

    def receive_all(self):
        buffer = ""
        while not buffer.endswith(modell.END_CHARACTER):
            buffer += self.sock.recv(BUFFER_SIZE).decode(modell.TARGET_ENCODING)

        return buffer[:-1]

    def send_end(self):
        message = modell.Message(username=self.username, message=messagess.END_GAME, quit=True)
        try:
            self.sock.sendall(message.marshal())
        except (ConnectionAbortedError, ConnectionResetError):
            if not self.closing:
                self.ui.alert(messagess.ERROR, messagess.CONNECTION_ERROR)

    def send(self):
        message = self.ui.message.get()
        if(self.allCard >=4):
            # self.ui.updateButton()
            self.ui.hill()


        self.allCard = self.allCard - 1
        self.cardRival = self.cardRival + int(message)
        self.ui.message.set("")
        message = modell.Message(username=self.username, message=message, quit=False)
        self.ui.forth_button['state'] = views.TEXT_STATE_DISABLED
        self.ui.third_button['state'] = views.TEXT_STATE_DISABLED
        self.ui.second_button['state'] = views.TEXT_STATE_DISABLED
        self.ui.first_button['state'] = views.TEXT_STATE_DISABLED
        try:
            self.sock.sendall(message.marshal())
        except (ConnectionAbortedError, ConnectionResetError):
            if not self.closing:
                self.ui.alert(messagess.ERROR, messagess.CONNECTION_ERROR)

    def exit(self):
        self.closing = True
        try:
            self.sock.sendall(modell.Message(username=self.username, message="", quit=True).marshal())
        except (ConnectionResetError, ConnectionAbortedError, OSError):
            print(messagess.CONNECTION_ERROR)
        finally:
            self.sock.close()
