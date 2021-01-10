from HTTPServer import HTTPServer
import socket


class Server1(HTTPServer):
    def start(self):

        try:
            while True:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                s.bind((self.host, self.port))
                s.listen(5)

                print("Listening at", s.getsockname())

                conn, addr = s.accept()
                print("Connected by", addr)
                s.close() # We close the socket so that no more client are able to connect.

                self.handle_single_connection(conn) # This function will communicate (/listen) to 1 single client

        except KeyboardInterrupt:
            quit() # Server stops at ctrl + c


if __name__ == '__main__':
    server = Server1()
    server.start()
