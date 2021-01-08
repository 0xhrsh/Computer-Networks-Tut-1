from HTTPRequest import HTTPRequest
from TCPServer import TCPServer



class HTTPServer(TCPServer):
    """The actual HTTP server class."""

    headers = {
        'Server': 'CrudeServer',
        'Content-Type': 'text/html',
    }

    status_codes = {
        200: 'OK',
        404: 'Not Found',
        501: 'Not Implemented',
    }

    def handle_request(self, data):
        """Handles incoming requests"""

        request = HTTPRequest(data) # Get a parsed HTTP request

        try:
            # Call the corresponding handler method for the current 
            # request's method
            handler = getattr(self, 'handle_%s' % request.method)
        except AttributeError:
            handler = self.HTTP_501_handler

        response = handler(request)
        return response

    def response_line(self, status_code):
        """Returns response line (as bytes)"""
        reason = self.status_codes[status_code]
        response_line = 'HTTP/1.1 %s %s\r\n' % (status_code, reason)

        return response_line.encode() # convert from str to bytes

    def response_headers(self, extra_headers=None):
    
        headers_copy = self.headers.copy() # make a local copy of headers

        if extra_headers:
            headers_copy.update(extra_headers)

        headers = ''

        for h in headers_copy:
            headers += '%s: %s\r\n' % (h, headers_copy[h])

        return headers.encode() # convert str to bytes

    def handle_OPTIONS(self, request):
        """Handler for OPTIONS HTTP method"""

        response_line = self.response_line(200)

        extra_headers = {'Allow': 'OPTIONS, GET'}
        response_headers = self.response_headers(extra_headers)

        blank_line = b'\r\n'

        return b''.join([response_line, response_headers, blank_line])

    def handle_GET(self, request):
        

        blank_line = b'\r\n'
        response_line = self.response_line(200)
        response_headers = self.response_headers()
        response_body = b'<h1>Server working fine!</h1>'
        response = b''.join([response_line, response_headers, blank_line, response_body])

        return response

    def HTTP_501_handler(self, request):
        """Returns 501 HTTP response if the requested method hasn't been implemented."""

        response_line = self.response_line(status_code=501)

        response_headers = self.response_headers()

        blank_line = b'\r\n'

        response_body = b'<h1>501 Not Implemented</h1>'

        return b"".join([response_line, response_headers, blank_line, response_body])
