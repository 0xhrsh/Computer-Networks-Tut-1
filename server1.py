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
                s.close()

                self.handle_single_connection(conn)

        except KeyboardInterrupt:
            quit()


if __name__ == '__main__':
    server = Server1()
    server.start()
