import bayeslite


db_pathname = 'foo.bdb'

with bayeslite.bayesdb_open(pathname=db_pathname) as bdb:
    # Create TestTable
    bdb.execute("DROP TABLE IF EXISTS testTable;")
    bdb.sql_execute('CREATE TABLE testTable(name TEXT, x INT, y INT);')
    # Fill it with some data
    bdb.sql_execute("INSERT INTO testTable VALUES('Alice', 1, 11);")
    bdb.sql_execute("INSERT INTO testTable VALUES('Bob', 2, 12);")
    bdb.sql_execute("INSERT INTO testTable VALUES('Candice', 3, 13);")

    # Print out Alice's row
    result = bdb.execute("SELECT * FROM testTable WHERE name='Alice';")
    print "Result of the query: "+result[0]+"\n"

    # Create a population with which to do a simulation
    pop = bdb.execute("CREATE POPULATION testPopulation FOR testTable WITH SCHEMA (SET STATTYPES OF x,y TO numerical, numerical; IGNORE name;);")  # Crashes on this query D:
    result = bdb.execute("SIMULATE y FROM testPopulation GIVEN x=2 LIMIT 20")
    print result
    print "\n"

    # Print out Alice's row again
    result = bdb.execute("SELECT * FROM testTable WHERE name='Alice';")
    print "Result of the query: " + result[0] + "\n"
