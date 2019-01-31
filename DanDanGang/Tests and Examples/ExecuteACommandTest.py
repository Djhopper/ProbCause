import bayeslite

db_pathname = 'foo.bdb'

result = None
with bayeslite.bayesdb_open(pathname=db_pathname) as bdb:
    bdb.execute("DROP TABLE testTable")
    bdb.sql_execute('CREATE TABLE testTable(name TEXT, x INT, y INT)')
    bdb.sql_execute("INSERT INTO testTable VALUES('Alice', 1, 11)")
    bdb.sql_execute("INSERT INTO testTable VALUES('Bob', 2, 12)")
    bdb.sql_execute("INSERT INTO testTable VALUES('Candice', 3, 13)")
    result = bdb.execute("SELECT * FROM testTable WHERE name='Alice'")

print result
for i in result:
    print(i)
