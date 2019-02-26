import bayeslite
import numpy.random as random
import pandas as pd
from tqdm import tqdm as tqdm

db_pathname = 'foo.bdb'


with bayeslite.bayesdb_open(pathname=db_pathname) as bdb:
    # Create and populate table
    data = pd.DataFrame(columns=['x', 'y', 'z'])
    simdata = pd.DataFrame(columns=['x', 'y', 'z'])
    bdb.sql_execute(
        "CREATE TABLE t(name TEXT, x INT, y INT, z INT);")
    print('generating data')
    for i in tqdm(range(10000)):
        name = random.choice(['Alice', 'Bob', 'Charlie'])
        x = random.randint(1, 50)
        y = random.randint(-5, 5) + random.uniform(0.75, 1.33) * x
	z = (x-random.rand()*2+1) ** 2 + y
	data = data.append({'x':x, 'y':y, 'z':z}, ignore_index=True)
        bdb.sql_execute("INSERT INTO t VALUES(?, ?, ?, ?);", (name, x, y, z))
    data.to_csv('data.csv')
    # Do simulation
    bdb.execute(
        "CREATE POPULATION p FOR t (ignore name; x numerical; y numerical; z numerical)")
    bdb.execute(
        "CREATE GENERATOR g FOR p")
    bdb.execute(
        "INITIALIZE 1 MODEL FOR g")
    print('test')	
    t = int(input("How long should we analyze for? "))
    bdb.execute(
        "ANALYZE g FOR "+str(t)+" SECONDS")
    result = bdb.execute(
        "SIMULATE x,y,z FROM p LIMIT 500")
	
    # Print results of simulation
    sim = result.fetchall()
    for i in sim:
        x,y,z = i
	simdata = simdata.append({'x':x, 'y':y, 'z':z}, ignore_index=True)
        print i
    simdata.to_csv('simdata{}.csv'.format(str(t)))
    # Clean-up
    bdb.execute("DROP GENERATOR IF EXISTS g;")
    bdb.execute("DROP POPULATION IF EXISTS p;")
    bdb.execute("DROP TABLE IF EXISTS t;")
