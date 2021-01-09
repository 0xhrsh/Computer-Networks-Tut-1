import socket
from HTTPRequest import HTTPRequest


class HTTPServer:
    
    def __init__(self, host='127.0.0.1', port=8888):
        self.host = host
        self.port = port

    status_codes = {
        200: 'OK',
        404: 'Not Found',
    }

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
                if data is None:
                    conn.close()
                    break       
                response = self.handle_request(data)
                conn.sendall(response)
                 
            

    def handle_request(self, data):
        
        request = HTTPRequest(data)

        operations = request.method.split()

        n = len(operations)
        ans = int(operations[0])
        i=0
        while i < n-1:
            if operations[i+1] == "+":
                ans +=int(operations[i+2])
            if operations[i+1] == "-":
                ans -=int(operations[i+2])
            if operations[i+1] == "*":
                ans *=int(operations[i+2])
            if operations[i+1] == "/":
                ans /=int(operations[i+2])
            i+=2



        response_body = bytes(ans)
        blank_line = b"\r\n"

        return b"".join([b"", b"", b"", response_body])
    

    def response_line(self, status_code):
        
        reason = self.status_codes[status_code]
        line = "HTTP/1.1 %s %s\r\n" % (status_code, reason)

        return line.encode()

    def response_headers(self, extra_headers=None):

        headers_copy = self.headers.copy() 

        if extra_headers:
            headers_copy.update(extra_headers)

        headers = ""

        for h in headers_copy:
            headers += "%s: %s\r\n" % (h, headers_copy[h])

        return headers.encode()