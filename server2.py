from HTTPServer import HTTPServer
import socket
import threading


class Server2(HTTPServer):

    def start(self):

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((self.host, self.port))
        s.listen(5)
        # Here we don't close the socket, therefore multiple clients can connect
        print("Listening at", s.getsockname())

        threads = []

        try:
            while True:
                conn, addr = s.accept()
                print("Connected by", addr) 
                t = threading.Thread( # we start a thread for each new client
                    target=self.handle_single_connection, args=(conn,), daemon=True) 
                t.start()
                threads.append(conn)

        except KeyboardInterrupt:
            s.close() # On pressing ctrl + c, we close all connections
            for conn in threads:
                conn.close()
            quit() # Then we shut down the server


if __name__ == '__main__':
    server = Server2()
    server.start()
