# probcause.client_side

## send_request.py

`send_request.py` is a command-line callable script that sends an HTTP request outlining a data base as well as the queries that are to be applied to it. 
Command line usage of `send_request.py` is as follows:

`python send_request.py --server=<ADDR>:<PORT> --db=<DB> --file=<QUERIES>`

Where ADDR is an IP address, PORT is the address on which the server listens for requests, DB is the name of the data base file which needs to be accessed (<name>.bdb) and QUERIES is a file which contains one or more queries in valid BQL. The file structure of queries is the following:
```
query1
*****
query2
*****
...
*****
queryn
```
where the queries are guaranteed to be executed in the given order, and line breaks within queries are permitted, so long as at least one query delimiter is always between two separate queries.

