import bayeslite
from conv_cursor_to_json import conv_cursor_to_json

db_pathname = 'foo.bdb'


with bayeslite.bayesdb_open(pathname=db_pathname) as bdb:
    # Create and populate table
    bdb.sql_execute('CREATE TABLE t(name TEXT, x INT, y INT);')
    for name, x, y in [['A', 1, 11], ['B', 2, 12], ['C', 3, 13]]:
        bdb.sql_execute("INSERT INTO t VALUES(?, ?, ?);", (name, x, y))
    # Grab all data
    result = bdb.execute(
        "SELECT * FROM t")
    # Convert to json
    json = conv_cursor_to_json(result)
    for j in json:
        print j
    # Clean up
    bdb.execute("DROP TABLE t")
