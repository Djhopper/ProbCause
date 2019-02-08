import probcause.server_side.server as server
import threading
import httplib
import json
import time

ip = '128.232.98.213'
port = 8082


def server_thread_function():
    server.main(ip, port)


def test_server():
    queries = \
        '''foo.bdb
SQL CREATE TABLE t (name TEXT, x INT, y INT);
SQL INSERT INTO t VALUES("A", 1, 2);
SQL INSERT INTO t VALUES("B", 3, 4);
SELECT * FROM t;
DROP TABLE t;'''
    expected = json.dumps(
        [[], [], [], [{"y": 2, "x": 1, "name": "A"}, {"y": 4, "x": 3, "name": "B"}], []]
    )
    # Run server
    server_thread = threading.Thread(target=server_thread_function, args=())
    server_thread.daemon = True
    server_thread.start()
    time.sleep(1)
    # Make request
    connection = httplib.HTTPConnection(ip, port)
    connection.request("POST", "/", queries)
    response = connection.getresponse().read()

    print "Response: " + str(response)
    print "Expected: " + str(expected)
    assert response == expected


def test_server_error():
    queries = \
        '''foo.bdb
CREATE CHAOS'''
    expected = "Syntax error near [CHAOS] after [CREATE]"
    # Run server
    server_thread = threading.Thread(target=server_thread_function, args=())
    server_thread.daemon = True
    server_thread.start()
    time.sleep(1)
    # Make request
    connection = httplib.HTTPConnection(ip, port)
    connection.request("POST", "/", queries)
    response = connection.getresponse().read()
    assert response == expected


if __name__ == '__main__':
    test_server()
    test_server_error()
