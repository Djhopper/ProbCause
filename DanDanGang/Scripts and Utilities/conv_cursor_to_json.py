import json
import bayeslite


def conv_cursor_to_json(cursor):
    A = cursor.fetchall()
    ds = []
    for row in A:
        d = {}
        for i, column in enumerate(row):
            d[cursor.description[i][0]] = column
        ds.append(d)
    print "ds:"
    print ds
    r = [(dict((cursor.description[i][0], value))
          for i, value in enumerate(row)) for row in A]
    print "r:"
    print r

    json_output = json.dumps(r)
    return json_output
