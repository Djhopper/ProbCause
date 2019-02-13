from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import bayeslite
from bayeslite import BQLError, BQLParseError, BayesDBException, BayesDBTxnError
from probcause.util.conv_cursor_to_json import conv_cursor_to_json
import json

"""
REQUESTS
Requests are 'text/http' and are in the following format:
    database_name.bdb
    query
    query2
    ...
    queryN
-Note that the queries should not contain new lines. 
-Note that if query is valid SQL but not valid BQL, query must take form of:
    SQL query

RESPONSES
Responses are 'text/http' in the case that an error occurs:
    error_information
    
Or 'application/json' in the normal case:
    [
        [response1 ],
        [response2 ],
        ...
        [response3 ]
    ]
"""


class RequestHandler(BaseHTTPRequestHandler):
    @staticmethod
    def text_to_queries(text):
        t = text.split("\n")
        assert len(t) > 1
        db_name = t[0]
        queries = t[1:]
        queries = [query for query in queries if query.strip(" ").strip("\n") != ""]  # Remove empty queries
        return db_name, queries

    @staticmethod
    def results_to_json(results):
        assert len(results) > 0
        return json.dumps(results)

    def send_err(self, err):
        print str(err)
        self.send_header('Content-type', 'text/http')
        self.end_headers()
        self.wfile.write(str(err))

    def do_POST(self):
        self.send_response(200)

        try:
            content_length = int(self.headers['Content-Length'])
            text = self.rfile.read(content_length).decode("utf8")
            db_name, queries = RequestHandler.text_to_queries(text)
        except UnicodeDecodeError:
            self.send_err("Error: Couldn't decode request, make sure it's utf8")
            return
        except AssertionError:
            self.send_err("Error: You must give at least 1 query.")
            return

        results = []
        with bayeslite.bayesdb_open(pathname=db_name) as bdb:
            for query in queries:
                print "doing a query..."
                try:
                    if query[0:3].upper() != "SQL":
                        res = conv_cursor_to_json(bdb.execute(query))
                        results.append(res)
                        print "Query1: " + query
                        print "Result1: " + res
                    else:
                        res = conv_cursor_to_json(bdb.sql_execute(query[4:]))
                        results.append(res)
                        print "Query2: " + query
                        print "Result2: " + res
                except (BQLError, BQLParseError, BayesDBException), e:
                    print "ERROR D:"
                    self.send_err(e)
                    return

        self.send_header('Content-type', 'application/json')
        self.end_headers()
        message = RequestHandler.results_to_json(results)
        self.wfile.write(message)


def main(ip, port):
    try:
        httpd = HTTPServer((ip, port), RequestHandler)
        print "Running server on (" + str(httpd.server_address)
        httpd.serve_forever()
    except KeyboardInterrupt:
        print "Stopping server."


if __name__ == '__main__':
    ip = '128.232.98.213'
    port = 8080
    main(ip, port)
