# send_request.py
'''

Given a file handle, as well as a client ID, sends contents of the 
file (assumed valid BQL) to server side for processing through HTTP
request.

'''
import httplib
import sys
import getopt


query_delimiter = '*****'

def queryfy(lines):
	# find and separate queries, based on query delimiter.
	qs = []
	tmp = []
	for line in lines:
		if( line == query_delimiter ):
			qs.append(tmp.join(' '))
		else:
			tmp.append(line)
	if(tmp != []):
		qs.append(tmp.join(' '))
	return qs

def run(server_address, server_port):
	args_given = sys.argv[1:]

	try:	
		opts, args = getopt.getopts(args_given, ['file=', 'query='])
	except getopt.GetOptError as err:
		print(err)
		sys.exit(1)
	
	if len(opts) == 0:
		print('Please provide either a file to read the query/queries from, or a string containing the query.')
		print('Usage: send_request.py [--file=<FILE>] [--query=<QUERY>]. Please provide at least one of these options.')
		sys.exit(2)
	

	for opt, val in opts:
		if (opt == '--file'):
			srcfile = val
			f = open(srcfile, 'r')
			lines = f.readlines()
			queries = [q for q in queryfy(lines) if q != '']
			msg = queries.join('\n')  # TODO Need .bdb name too
		elif (opt == '--query'):
			msg = val.replace('\n', ' ')

	conn = httplib.HTTPSConnection(server_address, server_port)
	conn.request("POST", "/", msg)
	
	response = conn.getresponse()
	print("Got response.")

if __name__ == "__main__":
	server_address = ''
	server_port = 443
	run(server_address, server_port)
