import bayeslite
from probcause.util.conv_cursor_to_json import conv_cursor_to_json
import json

db_pathname = 'foo.bdb'


def test_conv_cursor_to_json():
    with bayeslite.bayesdb_open(pathname=db_pathname) as bdb:
        # Create and populate table
        bdb.sql_execute('CREATE TABLE t(name TEXT, x INT, y INT);')
        for name, x, y in [['A', 1, 11], ['B', 2, 12], ['C', 3, 13]]:
            bdb.sql_execute("INSERT INTO t VALUES(?, ?, ?);", (name, x, y))
        # Grab all data
        result = bdb.execute(
            "SELECT * FROM t")
        # Convert to json
        result = conv_cursor_to_json(result, True)
        assert result == json.dumps([{"y": 11, "x": 1, "name": "A"}, {"y": 12, "x": 2, "name": "B"}, {"y": 13, "x": 3, "name": "C"}])
        # Clean up
        bdb.execute("DROP TABLE t")
