from probcause.util.table_from_csv import table_from_url, table_from_csv
import bayeslite

table_name = 'testTable'
db_pathname = 'foo.bdb'
url = 'https://query.data.world/s/3c26afdi4kinjoqe3idolsxxk2ph4b'  # from data.world
file_name = 'wc_forecasts.csv'

output1 = [
    "(u'2018-06-22 13:56:23 UTC', u'Brazil', u'E', 92.77421, 3.07229, 0.29255, 1.63175, 1.23547, 0.13278, 3.1247700000000003, 4.84411, 1.71934, 0.65263, 0.27308000000000004, 0.07429, 0, 0.92571, 0.65965, 0.45548999999999995, 0.29535, 0.1889, u'2018-06-22 13:57:55 UTC')",
    "(u'2018-06-22 13:56:23 UTC', u'Spain', u'B', 91.38864000000001, 3.27389, 0.4846, 1.6645299999999998, 1.22053, 0.11494000000000001, 2.27516, 5.95793, 3.6827699999999997, 0.56611, 0.41906000000000004, 0.014830000000000001, 0, 0.9851700000000001, 0.7397199999999999, 0.49728, 0.30724, 0.18647, u'2018-06-22 13:57:55 UTC')",
    "(u'2018-06-22 13:56:23 UTC', u'France', u'C', 86.48779, 2.7685299999999997, 0.54703, 2.54007, 0.25749, 0.20244, 2.76047, 4.7523, 1.99183, 0.79756, 0.20244, 0, 0, 1, 0.6470199999999999, 0.35063, 0.17142000000000002, 0.08782000000000001, u'2018-06-22 13:57:55 UTC')"
]

output2 = [
    "(u'2018-06-22 13:56:23 UTC', u'Brazil', u'E', 92.77421, 3.07229, 0.29255, 1.63175, 1.23547, 0.13278, 3.12477, 4.84411, 1.71934, 0.65263, 0.27308, 0.07429, 0, 0.92571, 0.65965, 0.45549, 0.29535, 0.1889, u'2018-06-22 13:57:55 UTC')",
    "(u'2018-06-22 13:56:23 UTC', u'Spain', u'B', 91.38864, 3.27389, 0.4846, 1.66453, 1.22053, 0.11494, 2.27516, 5.95793, 3.68277, 0.56611, 0.41906, 0.01483, 0, 0.98517, 0.73972, 0.49728, 0.30724, 0.18647, u'2018-06-22 13:57:55 UTC')",
    "(u'2018-06-22 13:56:23 UTC', u'France', u'C', 86.48779, 2.76853, 0.54703, 2.54007, 0.25749, 0.20244, 2.76047, 4.7523, 1.99183, 0.79756, 0.20244, 0, 0, 1, 0.64702, 0.35063, 0.17142, 0.08782, u'2018-06-22 13:57:55 UTC')"
]

with bayeslite.bayesdb_open(pathname=db_pathname) as bdb:
    table_from_url(bdb, table_name, url)
    result = bdb.execute('SELECT * FROM testTable LIMIT 3;')
    for i, x in enumerate(result):
        assert str(x) == output1[i]
    bdb.execute("DROP TABLE IF EXISTS " + table_name)


with bayeslite.bayesdb_open(pathname=db_pathname) as bdb:
    with open(file_name, 'r') as f:
        table_from_csv(bdb, table_name, f)
        result = bdb.execute('SELECT * FROM testTable LIMIT 3;')
        for i, x in enumerate(result):
            assert str(x) == output2[i]
    bdb.execute("DROP TABLE IF EXISTS " + table_name)
