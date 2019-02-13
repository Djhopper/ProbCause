import probcause.server_side.server as server
import probcause.client_side.send_request as send_request
import threading
import time
import os
import pytest
import sys

'''
This script tests the functionality of probcause.client_side.send_request. That is,
it tests the correct functionality of send_request.lines_to_queries() and 
send_request.run().
The tests that get conducted are 
    -- Check that lines_to_queries operates as expected on a collection of inputs
    -- Check that send_request.run() outputs the correct things and exits with 
       correct codes when called with erroneous / correct sys.argv
'''

ip = '128.232.98.213'
port = 8082


def server_thread_function():
    server.main(ip, port)


def test_lines_to_queries():
    test_files = ['test_query_files/' + f for f in os.listdir('test_query_files')]
    output_files = ['test_queries/' + f for f in os.listdir('test_queries')]
    for i, f in enumerate(test_files):
        print('Checking queryfication of ' + f)
        lines = open(name=f, mode='r').readlines()
        queries = send_request.lines_to_queries(lines)
	print(queries)
        assert queries == [s.replace('\n', '') for s in open(name=output_files[i], mode='r').readlines()]


def test_no_arguments():
    server_thread = threading.Thread(target=server_thread_function, args=())
    server_thread.daemon = True
    server_thread.start()
    time.sleep(0.5)  # XXX Bad way to ensure the server is definitely done setting up
    sys.argv = ['send_request.py']
    with pytest.raises(send_request.BadOptionsError) as e:
        send_request.main()
        
    response = (e.value.value, e.value.message)
    expected = (3, 'Please provide the db file to operate on.')
    assert response == expected


def test_bad_options():
    server_thread = threading.Thread(target=server_thread_function, args=())
    server_thread.daemon = True
    server_thread.start()
    time.sleep(0.5)  # XXX Bad way to ensure the server is definitely done setting up
    sys.argv = ['send_request.py', '--badoption']
    with pytest.raises(send_request.BadOptionsError) as e:
        send_request.main() 
    
    response = (e.value.value, e.value.message)
    expected = (1, 'Bad options given.')

    assert response == expected


def test_no_db():
    server_thread = threading.Thread(target=server_thread_function, args=())
    server_thread.daemon = True
    server_thread.start()
    time.sleep(0.5)  # XXX Bad way to ensure the server is definitely done setting up
    sys.argv = ['send_request.py', '--file=../tests/test_queries/1'] 
    with pytest.raises(send_request.BadOptionsError) as e:
        send_request.main() 
    
    response = (e.value.value, e.value.message)
    expected = (3, 'Please provide the db file to operate on.')

    assert response == expected


def test_no_query():
    server_thread = threading.Thread(target=server_thread_function, args=())
    server_thread.daemon = True
    server_thread.start()
    time.sleep(0.5)  # XXX Bad way to ensure the server is definitely done setting up
    expected = (2, 'Please provide either a file to read the query/queries from, or a string containing the query. Usage: send_request.py --db=<DB> [--file=<FILE>] [--query=<QUERY>]. Please provide at least one of the bracketed options.') 
    sys.argv = ['send_request.py', '--db=foo.bdb']
    with pytest.raises(send_request.BadOptionsError) as e:
        send_request.main()
    
    response = (e.value.value, e.value.message)

    assert expected == response 


def test_no_error_query_given():
    server_thread = threading.Thread(target=server_thread_function, args=())
    server_thread.daemon = True
    server_thread.start()
    time.sleep(0.5)  # XXX Bad way to ensure the server is definitely done setting up

    sys.argv = ['send_request.py', '--db=foo.bdb', '--query=\'DROP TABLE t;\'']

    send_request.main()


def test_no_error_file_given():
    server_thread = threading.Thread(target=server_thread_function, args=())
    server_thread.daemon = True
    server_thread.start()
    time.sleep(0.5)  # XXX Bad way to ensure the server is definitely done setting up

    sys.argv = ['send_request.py', '--db=foo.bdb', '--file=../tests/test_queries/1']

    send_request.main()
