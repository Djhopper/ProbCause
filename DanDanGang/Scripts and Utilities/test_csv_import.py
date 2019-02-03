from create_table_from_csv import table_from_csv_url, table_from_csv
import urllib2
import bayeslite

table_name = 'testTable'
db_pathname = 'foo.bdb'
url = 'https://data.chhs.ca.gov/dataset/e0216fbb-3739-4d92-9630-88d9f5686ac6/resource/cdb50347-6fe1-456e-a336-d7daf0aba595/download/road-traffic-injuries-2002-2010.csv'

print "Test 1:"
with bayeslite.bayesdb_open(pathname=db_pathname) as bdb:
    table_from_csv_url(bdb, table_name, url)
    result = bdb.execute('SELECT * FROM testTable LIMIT 10;')
    for i in result:
        print i


print "Test 2:"
with bayeslite.bayesdb_open(pathname=db_pathname) as bdb:
    with urllib2.urlopen(url) as f:
        table_from_csv(bdb, table_name, f)
        result = bdb.execute('SELECT * FROM testTable LIMIT 10;')
        for i in result:
            print i
