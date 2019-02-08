import probcause.server_side.server as server
import probcause.client_side.send_request as send_request
import threading
import httplib
import json
import time
import os
import subprocess

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
        lines = open(file=f, mode='r').readlines()
        queries = send_request.lines_to_queries(lines)
        assert queries == open(file=output_files[i], mode='r').readlines()


def test_no_arguments():
    server_thread = threading.Thread(target=server_thread_function, args=())
    server_thread.daemon = True
    server_thread.start()
    time.sleep(0.5)  # XXX Bad way to ensure the server is definitely done setting up

    process = subprocess.Popen(['python', '../client_side/send_request.py'],
                               stdout=subprocess.PIPE)
    
    response = (process.returncode, process.communicate())
    expected = (2, ['Please provide either a file to read the query/queries from, or a string containing the query.', 'Usage: send_request.py --db=<DB> [--file=<FILE>] [--query=<QUERY>]. Please provide at least one of the bracketed options.'])

    assert response == expected


def test_bad_options():
    server_thread = threading.Thread(target=server_thread_function, args=())
    server_thread.daemon = True
    server_thread.start()
    time.sleep(0.5)  # XXX Bad way to ensure the server is definitely done setting up
    
    process = subprocess.Popen(['python', '../client_side/send_request.py', '--badoption'], 
        stdout=subprocess.PIPE)
    
    response = process.returncode
    expected = 1

    assert response == expected


def test_no_db():
    server_thread = threading.Thread(target=server_thread_function, args=())
    server_thread.daemon = True
    server_thread.start()
    time.sleep(0.5)  # XXX Bad way to ensure the server is definitely done setting up
    
    process = subprocess.Popen(['python', '../client_side/send_request.py', '--file=../tests/test_queries/1'], 
        stdout=subprocess.PIPE)
    
    response = process.returncode
    expected = 3

    assert response == expected


def test_no_query():
    server_thread = threading.Thread(target=server_thread_function, args=())
    server_thread.daemon = True
    server_thread.start()
    time.sleep(0.5)  # XXX Bad way to ensure the server is definitely done setting up
    
    process = subprocess.Popen(['python', '../client_side/send_request.py', '--db=foo.db'], 
        stdout=subprocess.PIPE)
    
    response = process.returncode
    expected = 2

    assert response == expected


def test_no_error_query_given():
    server_thread = threading.Thread(target=server_thread_function, args=())
    server_thread.daemon = True
    server_thread.start()
    time.sleep(0.5)  # XXX Bad way to ensure the server is definitely done setting up
    
    process = subprocess.Popen(['python', '../client_side/send_request.py', '--db=foo.db', '--query=\'DROP TABLE t;\''], 
        stdout=subprocess.PIPE)
    
    response = process.returncode
    expected = 0

    assert response == expected


def test_no_error_file_given():
    server_thread = threading.Thread(target=server_thread_function, args=())
    server_thread.daemon = True
    server_thread.start()
    time.sleep(0.5)  # XXX Bad way to ensure the server is definitely done setting up
    
    process = subprocess.Popen(['python', '../client_side/send_request.py', '--db=foo.db', '--file=../tests/test_queries/1'], 
        stdout=subprocess.PIPE)
    
    response = process.returncode
    expected = 0

    assert response == expected
