import socket


class HTTPServer:
    
    def __init__(self, host='127.0.0.1', port=8888):
        self.host = host
        self.port = port

    def start(self):

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((self.host, self.port))
        s.listen(5)

        print("Listening at", s.getsockname())

        while True:
            conn, addr = s.accept()
            print("Connected by", addr)

            data = conn.recv(1024) 

            response = self.handle_request(data)

            conn.sendall(response)
            conn.close()


    def handle_request(self, data):
        
        request = HTTPRequest(data) # Get a parsed HTTP request

        operation = request.method

        response_body = b'<h1>Server working fine!</h1>'
        response = response_body

        return response

    