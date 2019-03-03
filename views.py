import tkinter
import messagess
from tkinter import messagebox, simpledialog

CLOSING_PROTOCOL = "WM_DELETE_WINDOW"
END_OF_LINE = "\n"
KEY_RETURN = "<Return>"
TEXT_STATE_DISABLED = "disabled"
TEXT_STATE_NORMAL = "normal"


class EzChatUI(object):
    def __init__(self, application):
        self.application = application
        self.gui = None
        self.frame = None
        self.input_field = None
        self.message = None
        self.message_list = None
        self.scrollbar = None
        self.send_button = None
        self.first_button = None
        self.second_button = None
        self.third_button = None
        self.forth_button = None
        self.r1=None
        self.r2=None
        self.r3 = None
        self.r4 = None



    def show(self):
        self.gui = tkinter.Tk() #создали класс для пользования библиотекой
        self.gui.title(messagess.TITLE)#заголовок
        self.fill_frame()# наполняем наше окно
        self.gui.protocol(CLOSING_PROTOCOL,self.on_closing)#получает два аргумента: название события и функцию, которая будет вызываться при наступлении указанного события
        return self.input_dialogs()# сообщения выводимые - по поводу сервака, порта и имени

    def loop(self):
        self.gui.mainloop() #  без неё не создается окно

    def fill_frame(self):
        self.frame = tkinter.Frame(self.gui) #предназначен для организации виджетов внутри окна

        self.scrollbar = tkinter.Scrollbar(self.frame)
        self.message_list = tkinter.Text(self.frame,state=TEXT_STATE_DISABLED,width=100, height=20)#  позволяет пользователю ввести любое количество текста
        self.scrollbar.pack(side=tkinter.RIGHT,fill=tkinter.Y) #прокрутить - правая сторона
        self.message_list.pack(side=tkinter.LEFT,fill=tkinter.BOTH)
        self.message = tkinter.StringVar()
        self.frame.pack()
        self.r1 = tkinter.Radiobutton(self.gui,text='-3', variable=self.message, value=-3)
        self.r1.pack()
        self.r2 = tkinter.Radiobutton(self.gui,text='-4', variable=self.message, value=-4)
        self.r2.pack()
        self.r3 = tkinter.Radiobutton(self.gui, text='-2', variable=self.message, value=-2)
        self.r3.pack()
        self.r4 = tkinter.Radiobutton(self.gui, text='-1', variable=self.message, value=-1)
        self.r4.pack()

        #self.input_field.bind(KEY_RETURN,self.application.send)#привязывает событие к какому-либо действию

        self.send_button = tkinter.Button(self.gui, text=messagess.SEND, command=self.application.send)
        self.send_button.pack() # размещение кнопки на платформе




    def change(event,self):
        event.message.set("0")
        #self.forth_button['text'] = "0" - эта строчка не работает - надо чтобы сюда пришло значение кнопки - чтобы отправить

    def input_dialogs(self): # simpledialog.askstring - импортированное окошка позволяющее ввести одну строку
        self.gui.lower()#размещает поверх всех других окон
        self.application.username = simpledialog.askstring(messagess.USERNAME, messagess.INPUT_USERNAME, parent=self.gui)
        if self.application.username is None:
            return False
        self.application.host =simpledialog.askstring(messagess.SERVER_HOST, messagess.INPUT_SERVER_HOST, parent=self.gui)
        if self.application.host is None:
            return False
        self.application.port =simpledialog.askinteger(messagess.SERVER_PORT, messagess.INPUT_SERVER_PORT, parent=self.gui)

        if self.application.port is None:
            return False
        return True

    def alert(self, title, message): # выводим сообщения в табличке...
         messagebox.showerror(title, message)



    def show_message(self, message):
        self.message_list.configure(state=TEXT_STATE_NORMAL)# вывод сообщения
        self.message_list.insert(tkinter.END,str(message) + END_OF_LINE)#добавить текст в конец сообщения

        self.message_list.configure(state=TEXT_STATE_DISABLED)# вывод сообщения


    def on_closing(self):
        self.application.exit()
        self.gui.destroy()# уничтожение виджета и всех его потомков
