import probcause.demos.server as server
import probcause.demos.client as client
import threading

ip = '128.232.98.213'
port = 8082


server_thread = threading.Thread(target=server.run, args=(port, ip))
server_thread.daemon = True
server_thread.start()

client.run(ip, port)
