from bayeslite import bayesdb_read_pandas_df, bayesdb_read_csv
import pandas as pd
import io
import requests


def table_from_csv(bdb, table_name, f):
    bayesdb_read_csv(bdb, table_name, f, header=True, create=True, ifnotexists=True)


def table_from_url(bdb, table_name, url):
    s = requests.get(url).content
    df = pd.read_csv(io.StringIO(s.decode('utf-8')))
    bayesdb_read_pandas_df(bdb, table_name, df, create=True, ifnotexists=True)
