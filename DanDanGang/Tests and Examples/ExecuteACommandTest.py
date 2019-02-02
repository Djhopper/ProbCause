import bayeslite, random

db_pathname = 'foo.bdb'

with bayeslite.bayesdb_open(pathname=db_pathname) as bdb:
    # Create TestTable
    bdb.execute("DROP POPULATION IF EXISTS testPopulation;")
    bdb.execute("DROP TABLE IF EXISTS testTable;")
    bdb.sql_execute('CREATE TABLE testTable(name TEXT, x INT, y INT);')

    # Fill it with some data
    for i in range(100):
        name = random.choice(['A', 'B', 'C'])
        x = random.randint(1, 5)
        y = x + 8 + random.randint(1, 3)
        bdb.sql_execute("INSERT INTO testTable VALUES(?, ?, ?);", (name, x, y))

    # Create a population with which to do a simulation
    # bdb.execute(
    #    "CREATE POPULATION IF NOT EXISTS testPopulation FOR testTable WITH SCHEMA (MODEL x,y AS NUMERICAL; IGNORE name;);")
    bdb.execute(
        "CREATE POPULATION IF NOT EXISTS testPopulation FOR testTable WITH SCHEMA (GUESS STATTYPES FOR (*));")
    result = bdb.execute(
        "SIMULATE x,y FROM testPopulation LIMIT 20;")  # TODO: This returns an empty cursor, but shouldn't
    # result = bdb.execute("DEPENDENCE PROBABILITY OF y WITH x")
    print result.fetchall()
    for i in result.fetchall():
        print i