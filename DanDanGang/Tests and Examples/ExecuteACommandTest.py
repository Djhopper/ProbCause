import bayeslite

db_pathname = 'foo.bdb'

result = None
with bayeslite.bayesdb_open(pathname='foo.bdb') as bdb:
    result = bdb.execute('SELECT 42')

if result is not None:
    print result
else:
    print "failure"
