import bayeslite
import random

db_pathname = 'foo.bdb'


with bayeslite.bayesdb_open(pathname=db_pathname) as bdb:
    # Create and populate table
    bdb.sql_execute(
        "CREATE TABLE t(name TEXT, x INT, y INT);")
    for i in range(100):
        name = random.choice(['Alice', 'Bob', 'Charlie'])
        x = random.randint(1, 5)
        y = random.randint(1, 3) + 8 + x
        bdb.sql_execute("INSERT INTO t VALUES(?, ?, ?);", (name, x, y))

    # Do simulation
    bdb.execute(
        "CREATE POPULATION p FOR t (ignore name; x numerical; y numerical)")
    bdb.execute(
        "CREATE GENERATOR g FOR p")
    bdb.execute(
        "INITIALIZE 1 MODEL FOR g")
    t = int(input("How long should we analyze for? "))
    bdb.execute(
        "ANALYZE g FOR "+str(t)+" SECONDS")
    result = bdb.execute(
        "SIMULATE x,y FROM p LIMIT 50")

    # Print results of simulation
    sim = result.fetchall()
    for i in sim:
        print i

    # Clean-up
    bdb.execute("DROP GENERATOR IF EXISTS g;")
    bdb.execute("DROP POPULATION IF EXISTS p;")
    bdb.execute("DROP TABLE IF EXISTS t;")
