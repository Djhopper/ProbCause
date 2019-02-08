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


def queryfy_old(lines):  # Deprecated TODO Remove this?
	# find and separate queries, based on query delimiter.
	queries = []
	query = []
	for line in lines:
		if line == query_delimiter:
			queries.append(" ".join(query))
		else:
			query.append(line)
	if query != []:
		queries.append(" ".join(query))
	return queries


def lines_to_queries(lines):
	whole_file = " ".join(lines)
	queries = [query.replace("\n", " ") for query in whole_file.split(query_delimiter)]
	queries = [q for q in queries if q != '']  # Filter out empty queries
	return queries


def run(server_address, server_port):
	# Process command line inputs
	args_given = sys.argv[1:]

	try:	
		opts, args = getopt.getopt(args_given, ['file=', 'query='])
	except getopt.GetoptError as err:
		print(err)
		sys.exit(1)
	
	if len(opts) == 0:
		print('Please provide either a file to read the query/queries from, or a string containing the query.')
		print('Usage: send_request.py [--file=<FILE>] [--query=<QUERY>]. Please provide at least one of these options.')
		sys.exit(2)
	
	# Generate message for http request
	for opt, val in opts:  # TODO Should this loop ever run more than once? If so, should it be overwriting msg each time?
		if opt == '--file':
			f = open(file=val, mode='r')
			queries = lines_to_queries(f.readlines())
			msg = "\n".join(queries)  # TODO Need .bdb name too
		elif opt == '--query':
			msg = val.replace('\n', ' ')

	conn = httplib.HTTPSConnection(server_address, server_port)
	conn.request("POST", "/", msg)
	
	response = conn.getresponse()  # TODO Do something with response
	print("Got response.")


if __name__ == "__main__":
	server_address = ''
	server_port = 443
	run(server_address, server_port)
