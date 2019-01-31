from http.server import BaseHTTPRequestHandler, HTTPServer


class RequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        self.send_response(200)  # status code (200 means 'OK')

        # read in data from client's request
        content_length = int(self.headers['Content-Length'])
        name = self.rfile.read(content_length).decode("utf8")

        # set up headers
        self.send_header('Content-type', 'text/http')
        # info about what types of data you can send:
        # https://developer.mozilla.org/en-US/docs/Web/HTTP/Basics_of_HTTP/MIME_types/Complete_list_of_MIME_types
        self.end_headers()

        # output result back to client
        message = "Hello " + name
        self.wfile.write(bytes(message, "utf8"))


def run(port, ip, server_class=HTTPServer, handler_class=RequestHandler, ):
    server_address = (ip, port)
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()


if __name__ == "__main__":
    run(8081, '127.0.0.1')
