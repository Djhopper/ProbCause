from create_table_from_csv import table_from_url, table_from_csv
import bayeslite

table_name = 'testTable'
db_pathname = 'foo.bdb'
url = 'https://query.data.world/s/3c26afdi4kinjoqe3idolsxxk2ph4b'  # from data.world
file_name = 'wc_forecasts.csv'

print "Test 1:"
with bayeslite.bayesdb_open(pathname=db_pathname) as bdb:
    table_from_url(bdb, table_name, url)
    result = bdb.execute('SELECT * FROM testTable LIMIT 3;')
    for i in result:
        print i


print "Test 2:"
with bayeslite.bayesdb_open(pathname=db_pathname) as bdb:
    with open(file_name, 'r') as f:
        table_from_csv(bdb, table_name, f)
        result = bdb.execute('SELECT * FROM testTable LIMIT 3;')
        for i in result:
            print i
