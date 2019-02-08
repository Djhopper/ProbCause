import probcause.server_side.server as server
import threading
import httplib
import json

port = 8082


def server_thread():
    server.main('', port)


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
    th = threading.Thread(target=server_thread())
    th.daemon = True
    th.start()
    # Make request
    connection = httplib.HTTPConnection('', port)
    connection.request("POST", "/", queries)
    response = connection.getresponse()
    assert response == expected


if __name__ == '__main__':
    test_server()
