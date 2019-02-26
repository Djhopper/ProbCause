#!/home/oscar/miniconda/envs/probcomp/bin/python
import socket
import probcause.server_side.server as server
import time
while True:
	try:
		time.sleep(10)
		server.main('', 8082)
	except socket.error as e:
		if e.errno == 98:
			pass
		else:
			print(e)
