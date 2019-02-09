import probcause.server_side.server as server
import probcause.client_side.send_request as send_request
import threading
import httplib
import json
import time
import os
import subprocess
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


# TODO Read and then destroy this function
def dan_being_a_dick():
    import pytest
    with pytest.raises(SystemExit) as e:  # Syntax for catching errors
        pass
    assert e.type == SystemExit
    assert e.value.code == 5

    # In python, raising errors/exceptions is generally preferred to sys.exit() as errors/exceptions are less opaque
    # Also, normally your "run" function in send_request would take the form:
    #       def run(server_address, server_port, database_handle, queries=None, file=None):
    # This is so that argv ugliness doesn't get into the body of your code where it can be avoided.
    # (You put the argv stuff in the 'if __name__ == "__main__":' bit)

    # That said, who gives a f**k? Why am I being so extra?
    # Nobody knows...
    # It doesn't matter at all...
    # Yikes I'm a python-head how gross
    # - Dan

    # PS: These tests look fine.


def test_lines_to_queries():
    test_files = ['test_query_files/' + f for f in os.listdir('test_query_files')]
    output_files = ['test_queries/' + f for f in os.listdir('test_queries')]
    for i, f in enumerate(test_files):
        print('Checking queryfication of ' + f)
        lines = open(name=f, mode='r').readlines()
        queries = send_request.lines_to_queries(lines)
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
    
    success = True
    sys.argv = ['send_request.py', '--db=foo.db', '--query=\'DROP TABLE t;\'']
    try:
        send_request.main()
    except Exception as e:
        success = False

    assert success


def test_no_error_file_given():
    '''
    server_thread = threading.Thread(target=server_thread_function, args=())
    server_thread.daemon = True
    server_thread.start()
    time.sleep(0.5)  # XXX Bad way to ensure the server is definitely done setting up
    '''
    success = True
    sys.argv = ['send_request.py', '--db=foo.db', '--file=../tests/test_queries/1']
    try:
        send_request.main()
    except Exception as e:
        success = False

    assert success 
