from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import bayeslite

# Documentation for bayeslite:
# http://probcomp.csail.mit.edu/dev/bayesdb/doc/api.html

escape_char = '\n'
'''
Assuming requests are of the form:
    "foo.bdb
    QUERY_1
    QUERY_2
    ...
    QUERY_N"
'''


class RequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        self.send_response(200)

        content_length = int(self.headers['Content-Length'])
        request = self.rfile.read(content_length).decode("utf8").split(escape_char)

        db_pathname = request[0]
        queries = request[1:]

        # TODO
        with bayeslite.bayesdb_open(pathname=db_pathname) as bdb:
            for query in queries:
                result = bdb.execute(query)
        # TODO

        self.send_header('Content-type', 'text/http')
        self.end_headers()
        message = "Can't fill your request (not implemented)"
        self.wfile.write(bytes(message))


def run_server(port, ip):
    httpd = HTTPServer((ip, port), RequestHandler)
    httpd.serve_forever()




