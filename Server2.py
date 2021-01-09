from HTTPServer import HTTPServer
import socket
import threading


class Server2(HTTPServer):

    def listen(self, conn):
        while True:
            try:
                data = conn.recv(1024) 
            except socket.error:
                conn.close()
                break               
            if data == "":
                conn.close()
                break       
            response = self.handle_request(data)
            conn.sendall(response)


    def start(self):

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((self.host, self.port))
        s.listen(5)

        print("Listening at", s.getsockname())

        while True:
            conn, addr = s.accept()
            print("Connected by", addr)
            t = threading.Thread(target=self.listen, args=(conn,))
            t.start()


if __name__ == '__main__':
    server = Server2()
    server.start()