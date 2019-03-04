import socket
import probcause.src.server_side.server as server
import time
"""Runs indefinitely, restarting the server if/when it crashes"""
while True:
	try:
		server.main('', 8082)
		time.sleep(10)
	except socket.error as e:
		if e.errno == 98:
			pass
		else:
			print(e)