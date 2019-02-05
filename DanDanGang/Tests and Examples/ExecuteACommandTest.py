import bayeslite

db_pathname = 'foo.bdb'

with bayeslite.bayesdb_open(pathname=db_pathname) as bdb:
    # Create TestTable
    bdb.sql_execute('CREATE TABLE t(name TEXT, x INT, y INT);')

    # Fill it with some data
    for name, x, y in [['A', 1, 11], ['B', 2, 12], ['C', 3, 13]]:
        bdb.sql_execute("INSERT INTO testTable VALUES(?, ?, ?);", (name, x, y))

    bdb.execute(
        "CREATE POPULATION p FOR t (ignore name; x numerical; y numerical)")
    bdb.execute(
        "CREATE GENERATOR g FOR p USING crosscat()")
    result = bdb.execute(
        "SIMULATE x,y FROM p LIMIT 5")

    print result.fetchall()

with bayeslite.bayesdb_open(pathname=db_pathname) as bdb:
    # Clean-up
    bdb.execute("DROP POPULATION IF EXISTS testPopulation;")
    bdb.execute("DROP TABLE IF EXISTS testTable;")
