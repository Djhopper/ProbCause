# send_request.py
import httplib
import sys
import getopt

"""
Given a file handle, as well as a client ID, sends contents of the 
file (assumed valid BQL) to server side for processing through HTTP
request.
"""

query_delimiter = '*****'


class BadOptionsError(Exception):
    def __init__(self, message, num):
        super(BadOptionsError, self).__init__(message, num)
        self.value = num
        self.message = message


def lines_to_queries(lines):
    whole_file = " ".join(lines)
    queries = [query.replace("\n", " ").replace('  ', ' ') for query in whole_file.split(query_delimiter)]  # XXX bad way of getting rid of double spaces (couldn't figure out why it didn't work otherwise.)
    # strip() without arguments strips leading/trailing whitespace from a string.
    queries = [q.strip().replace('  ', ' ') for q in queries if q.strip() != '']  # Filter out empty queries
    return queries


def run(msg, server_address='128.232.98.213', server_port=8082):
    conn = httplib.HTTPConnection(server_address, server_port)

    conn.request("POST", "/", msg)

    response = conn.getresponse().read()
    return response


def main(args_given=None):
    if args_given is None:
        args_given = sys.argv[1:]
    print "args given: " + str(args_given)
    server_address = '128.232.98.213'
    server_port = 8082

    try:
        opts, args = getopt.getopt(args_given, '', ['db=', 'file=', 'query=', 'server='])
    except getopt.GetoptError:
        raise BadOptionsError('Bad options given.', 1)

    db_given = False
    msg = ''
    for opt, val in opts:
        if opt == '--file':
            f = open(name=val, mode='r')
            queries = lines_to_queries(f.readlines())
            msg += "\n".join(queries) + '\n'
        elif opt == '--query':
            msg += val.replace('\n', ' ') + '\n'
        elif opt == '--db':
            db_given = True
            db_file = val
        elif opt == '--server':
            (server_address, server_port) = val.split(':')

    if msg[-2:] == '\n':
        msg = msg[:-2]

    if not db_given:
        msg = "Please provide the db file to operate on."
        raise BadOptionsError(msg, 3)

    if msg == '':
        msg = 'Please provide either a file to read the query/queries from, or a string containing the query. Usage: send_request.py --db=<DB> [--file=<FILE>] [--query=<QUERY>]. Please provide at least one of the bracketed options.'
        raise BadOptionsError(msg, 2)

    msg = db_file + '''\n''' + msg
    return run(msg, server_address=server_address, server_port=server_port)


if __name__ == "__main__":
    main()
