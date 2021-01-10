import socket
from HTTPRequest import HTTPRequest

FORMAT_STRING = "Please give operation in the correct form. Example: 1 <space> + <space> 2".encode('utf8')


class HTTPServer: # This is an abstract class, we make server1 and server2 using this abstract class

    def __init__(self, host='127.0.0.1', port=8888):
        self.host = host
        self.port = port

    def handle_single_connection(self, conn):
        while True:
            try:
                data = conn.recv(1024)
            except socket.error:
                conn.close()
                break
            if data == b"" or data == b"quit\n":
                conn.close() # Client disconnects at typing "quit" or pressing ctrl + c
                break
            response = self.handle_request(data) # here we calculate the operation
            conn.sendall(response)

    def start(self):
        # To be defined in server files
        return

    def handle_request(self, data):

        request = HTTPRequest(data)

        operations = request.method.split() # We assume the operands will be space seperated

        n = len(operations)

        if (n-1) % 2 != 0:
            return FORMAT_STRING

        try:
            ans = int(operations[0])
        except:
            return FORMAT_STRING

        i = 0
        try:
            while i < n-1:
                if operations[i+1] == "+":
                    ans += int(operations[i+2])
                elif operations[i+1] == "-":
                    ans -= int(operations[i+2])
                elif operations[i+1] == "*":
                    ans *= int(operations[i+2])
                elif operations[i+1] == "/":
                    ans /= int(operations[i+2])
                else:
                    return FORMAT_STRING
                i += 2
        except:
            return FORMAT_STRING

        return str(ans).encode('utf8')
