from estimate_setup import db_handle
import bayeslite
import probcause.server_side.server as server
import probcause.client_side.send_request as send_request
import threading
import time

ip = '128.232.98.213'
port = 8082


def server_thread_function():
    server.main(ip, port)


def main():
    server_thread = threading.Thread(target=server_thread_function, args=())
    server_thread.daemon = True
    server_thread.start()
    time.sleep(0.5)  # XXX Bad way to ensure the server is definitely done setting up

    args = ['--db=GenderPayGap.bdb', '--file=queries/query']
    send_request.main(args)


if __name__ == "__main__":
    main()
