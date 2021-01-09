from HTTPServer import HTTPServer
import socket

class Server1(HTTPServer):
    def start(self):

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((self.host, self.port))
        s.listen(5)

        print("Listening at", s.getsockname())

        while True:
            conn, addr = s.accept()
            print("Connected by", addr)

            while True:
                try:
                    data = conn.recv(1024) 
                except socket.error:
                    conn.close()
                    break    
                print(data)           
                if data == "":
                    conn.close()
                    break       
                response = self.handle_request(data)
                conn.sendall(response)


if __name__ == '__main__':
    server = Server1()
    server.start()