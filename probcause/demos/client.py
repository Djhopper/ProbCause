import httplib


def run(ip, port):
    print 1
    # make connection
    connection = httplib.HTTPConnection(ip, port)
    print 2
    # make request
    connection.request("POST", "/", raw_input("Please input your name:\n"))
    print 3
    # get response
    response = connection.getresponse()
    print(response.read().decode("utf-8"))


if __name__ == "__main__":
    run('127.0.0.1', 8081)
