import tornado.ioloop
import tornado.httpserver
import tornado.options

from settings import *


def main():
    application.listen(SERVER_PORT)
    print("The server is running at http://127.0.0.1:%s" % SERVER_PORT)

    tornado.ioloop.IOLoop.current().start()

if __name__ == "__main__":
    main()
