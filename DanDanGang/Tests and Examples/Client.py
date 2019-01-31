import http.client


def run(ip, port):
    # make connection
    connection = http.client.HTTPConnection(ip, port)

    # make request
    connection.request("POST", "/", input("Please input your name:\n"))

    # get response
    response = connection.getresponse()
    print(response.read().decode("utf-8"))


if __name__ == "__main__":
    run('127.0.0.1', 8081)
