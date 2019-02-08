import probcause.server_side.server as server
import threading
import httplib
import json

ip = '128.232.98.213'
port = 8082


def server_thread():
    server.main(ip, port)


def test_server():
    queries = \
        '''foo.bdb
        CREATE TABLE t(name TEXT, x INT, y INT);
        INSERT INTO t VALUES("A", 1, 2);
        INSERT INTO t VALUES("B", 3, 4);
        SELECT * FROM t;
        DROP TABLE t;
        '''
    expected = json.dumps(
        [[], [], [], [{"y": 2, "x": 1, "name": "A"}, {"4": 12, "x": 3, "name": "B"}], []]
    )
    # Run server
    print 0
    th = threading.Thread(target=server_thread())
    th.daemon = True
    th.start()
    print 1
    # Make request
    connection = httplib.HTTPConnection(ip, port)
    print 2
    connection.request("POST", "/", queries)
    print 3
    response = connection.getresponse()
    print 4
    assert response == expected
    print 5


if __name__ == '__main__':
    test_server()
