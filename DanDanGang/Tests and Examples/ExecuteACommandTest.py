import bayeslite

db_pathname = 'foo.bdb'

with bayeslite.bayesdb_open(pathname=db_pathname) as bdb:
    # Clean-up
    bdb.execute("DROP GENERATOR IF EXISTS g;")
    bdb.execute("DROP POPULATION IF EXISTS p;")
    bdb.execute("DROP TABLE IF EXISTS t;")

with bayeslite.bayesdb_open(pathname=db_pathname) as bdb:
    # Create TestTable
    bdb.sql_execute('CREATE TABLE t(name TEXT, x INT, y INT);')

    # Fill it with some data
    for name, x, y in [['A', 1, 11], ['B', 2, 12], ['C', 3, 13]]:
        bdb.sql_execute("INSERT INTO t VALUES(?, ?, ?);", (name, x, y))

    bdb.execute(
        "CREATE POPULATION p FOR t (ignore name; x numerical; y numerical)")
    bdb.execute(
        "CREATE GENERATOR g FOR p")
    bdb.execute(
        "INITIALIZE 1 MODEL FOR g")
    bdb.execute(
        "ANALYZE g FOR 10 SECONDS")
    result = bdb.execute(
        "SIMULATE x,y FROM p LIMIT 5")

    print result.fetchall()

with bayeslite.bayesdb_open(pathname=db_pathname) as bdb:
    # Clean-up
    bdb.execute("DROP GENERATOR IF EXISTS g;")
    bdb.execute("DROP POPULATION IF EXISTS p;")
    bdb.execute("DROP TABLE IF EXISTS t;")
