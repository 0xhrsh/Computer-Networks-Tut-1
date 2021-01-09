from HTTPServer import HTTPServer
import socket

class Server1(HTTPServer):
    def start(self):

        while True:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind((self.host, self.port))
            s.listen(5)

            print("Listening at", s.getsockname())

        
            conn, addr = s.accept()
            print("Connected by", addr)
            s.close()

            while True:
                try:
                    data = conn.recv(1024) 
                except socket.error:
                    break    
 
                if data == "":        
                    break       
                response = self.handle_request(data)
                conn.sendall(response)

            conn.close()


if __name__ == '__main__':
    server = Server1()
    server.start()