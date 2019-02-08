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


def lines_to_queries(lines):
	whole_file = " ".join(lines)
	queries = [query.replace("\n", " ") for query in whole_file.split(query_delimiter)]
	queries = [q for q in queries if q != '']  # Filter out empty queries
	return queries


def run(server_address, server_port):
	# Process command line inputs
	args_given = sys.argv[1:]

	try:	
		opts, args = getopt.getopt(args_given, '', ['db=', 'file=', 'query='])
	except getopt.GetoptError as err:
		print(err)
		sys.exit(1)
	
	if len(opts) == 0:
		print('Please provide either a file to read the query/queries from, or a string containing the query.')
		print('Usage: send_request.py --db=<DB> [--file=<FILE>] [--query=<QUERY>]. Please provide at least one of the bracketed options.')
		sys.exit(2)

	db_given = False
	msg = ''
	for opt, val in opts:  
		if opt == '--file':
			f = open(file=val, mode='r')
			queries = lines_to_queries(f.readlines())
			msg += "\n".join(queries) + '\n'  
		elif opt == '--query':
			msg += val.replace('\n', ' ') + '\n'
		elif opt == '--db':
			db_given = True
			db_file = val
	if msg[-2:] == '\n':
		msg = msg[:-2]
	
	if not db_given:
		print("Please provide the db file to operate on.")
		sys.exit(3)

	conn = httplib.HTTPSConnection(server_address, server_port)
	conn.request("POST", "/", db_file + '\n' + msg)
	
	response = conn.getresponse()  # TODO Do something with response
	print("Got response.")


if __name__ == "__main__":
	server_address = '128.232.98.213'
	server_port = 443
	run(server_address, server_port)
