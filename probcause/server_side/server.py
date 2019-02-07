from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import bayeslite
from bayeslite import BQLError, BQLParseError, BayesDBException, BayesDBTxnError
from probcause.util.conv_cursor_to_json import conv_cursor_to_json
import json

"""
REQUESTS
Requests are 'text/http' and are in the following format:
    database_name.bdb
    query1
    query2
    ...
    queryN
Note that the queries should not contain new lines. 

RESPONSES
Responses are 'text/http' in the case that an error occurs:
    error_information
    
Or 'application/json' in the normal case:
    [
        {response1 },
        {response2 },
        ...
        {response3}
    ]
"""


class RequestHandler(BaseHTTPRequestHandler):
    @staticmethod
    def text_to_queries(text):
        t = text.split("\n")
        assert len(t) > 1
        db_name = t[0]
        queries = t[1:]
        return db_name, queries

    @staticmethod
    def results_to_json(results):
        assert len(results > 0)
        return json.dumps(results)

    def do_POST(self):
        self.send_response(200)

        err = False

        try:
            content_length = int(self.headers['Content-Length'])
            text = self.rfile.read(content_length).decode("utf8")
            db_name, queries = RequestHandler.text_to_queries(text)
        except UnicodeDecodeError:
            err = "Error: Couldn't decode request, make sure it's utf8"
        except AssertionError:
            err = "Error: You must give at least 1 query."

        if not err:
            results = []
            with bayeslite.bayesdb_open(pathname=db_name) as bdb:
                for query in queries:
                    try:
                        results.append(conv_cursor_to_json(bdb.execute(query)))
                    except (BQLError, BQLParseError, BayesDBException), e:
                        err = e
                        break

        if not err:
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            message = RequestHandler.results_to_json(results)
        else:
            self.send_header('Content-type', 'text/http')
            self.end_headers()
            message = str(err)

        self.wfile.write(message)


def main(ip, port):
    try:
        httpd = HTTPServer((ip, port), RequestHandler)
        print "Running server..."
        httpd.serve_forever()
    except KeyboardInterrupt:
        print "Stopping server."


if __name__ == '__main__':
    main('', 443)
