import sys
import application

def main(args):
    app = application.Application(args)# создали объект класса- переход в Init
    app.execute()
if __name__ == "__main__":
    main('sug')


