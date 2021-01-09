import socket
from HTTPRequest import HTTPRequest

FORMAT_STRING = "Please give operation in the correct form: num1<space>+<space>num2<space>/<space>num3.\n All other operations are invalid".encode('utf8')

class HTTPServer:
    
    def __init__(self, host='127.0.0.1', port=8888):
        self.host = host
        self.port = port

    status_codes = {
        200: 'OK',
        404: 'Not Found',
    }

    def handle_single_connection(self, conn):
        while True:
            try:
                data = conn.recv(1024) 
            except socket.error:
                conn.close()
                break               
            if data == b"" or data == b"quit":
                conn.close()
                break       
            response = self.handle_request(data)
            conn.sendall(response)

    def start(self):
        # To be defined in server files
        return
                 

    def handle_request(self, data):
        
        request = HTTPRequest(data)

        operations = request.method.split()

        n = len(operations)

        if (n-1)%2 != 0:
            return FORMAT_STRING

        try:
            ans = int(operations[0])
        except:
            return FORMAT_STRING

        i=0
        try:
            while i < n-1:
                if operations[i+1] == "+":
                    ans +=int(operations[i+2])
                elif operations[i+1] == "-":
                    ans -=int(operations[i+2])
                elif operations[i+1] == "*":
                    ans *=int(operations[i+2])
                elif operations[i+1] == "/":
                    ans /=int(operations[i+2])
                else:
                    return FORMAT_STRING
                i+=2
        except :
            return FORMAT_STRING

        return str(ans).encode('utf8')
    
    