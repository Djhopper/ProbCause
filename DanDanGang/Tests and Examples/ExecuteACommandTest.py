import bayeslite

db_pathname = 'foo.bdb'

with bayeslite.bayesdb_open(pathname=db_pathname) as bdb:
    bdb.execute("DROP TABLE IF EXISTS testTable;")
    bdb.sql_execute('CREATE TABLE testTable(name TEXT, x INT, y INT);')
    bdb.sql_execute("INSERT INTO testTable VALUES('Alice', 1, 11);")
    bdb.sql_execute("INSERT INTO testTable VALUES('Bob', 2, 12);")
    bdb.sql_execute("INSERT INTO testTable VALUES('Candice', 3, 13);")
    result = bdb.execute("SELECT * FROM testTable WHERE name='Alice';")
    for i in result:
        print i
    print()

    #pop = bdb.execute("CREATE POPULATION testPopulation FOR testTable WITH SCHEMA (SET STATTYPES OF x,y TO numerical, numerical; IGNORE name;)")
    #result = bdb.execute("SIMULATE y FROM testPopulation GIVEN x=2 LIMIT 20")
    result = bdb.execute("PROBABILITY DENSITY OF x GIVEN y=2;")
    print result
    print()

    result = bdb.execute("SELECT * FROM testTable WHERE name='Alice';")
    for i in result:
        print i
    print()


