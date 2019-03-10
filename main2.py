import sys
import application

def main(args):
    app = application.Application(args)
    app.execute()


if __name__ == "__main__":
    main('sug')


