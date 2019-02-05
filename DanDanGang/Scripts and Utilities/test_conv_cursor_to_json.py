import json
import bayeslite

db_pathname = 'foo.bdb'


with bayeslite.bayesdb_open(pathname=db_pathname) as bdb:
    # Create TestTable
    bdb.sql_execute('CREATE TABLE t(name TEXT, x INT, y INT);')

    # Fill it with some data
    for name, x, y in [['A', 1, 11], ['B', 2, 12], ['C', 3, 13]]:
        bdb.sql_execute("INSERT INTO t VALUES(?, ?, ?);", (name, x, y))

    result = bdb.execute(
        "SELECT * FROM t"
    )
    print conv_cursor_to_json(result)
