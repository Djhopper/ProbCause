from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import bayeslite


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

        client_ip = self.client_address[0]
        print "Received query from: "+str(client_ip)

        db_pathname = request[0]
        queries = request[1:]

        with bayeslite.bayesdb_open(pathname=db_pathname) as bdb:
            for i, query in enumerate(queries[:-1]):
                print "Executing query "+str(i)
                bdb.execute(query)
            print "Executing final query"
            result = bdb.execute(queries[-1])

        self.send_header('Content-type', 'text/http')
        self.end_headers()
        message = "Can't fill your request (not implemented)"
        self.wfile.write(bytes(message))


def run_server(port, ip):
    httpd = HTTPServer((ip, port), RequestHandler)
    httpd.serve_forever()




