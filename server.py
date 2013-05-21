import config
import tornado.ioloop
from modules.servers import ExpectTCPServer, ExpectIMAPServer

if __name__ == '__main__':
    https_server = ExpectTCPServer(ssl_options=config.ssl_options)
    https_server.listen(443)

    imap_server = ExpectIMAPServer(ssl_options=config.ssl_options)
    imap_server.listen(993)

    tornado.ioloop.IOLoop.instance().start()
