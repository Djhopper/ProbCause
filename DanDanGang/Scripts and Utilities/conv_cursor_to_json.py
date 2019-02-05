import json
import bayeslite


def conv_cursor_to_json(cursor):
    d = {}
    for row in cursor.fetchall():
        for i, column in enumerate(row):
            d[cursor.description[i][0]] = column
    print d
    r = [(dict((cursor.description[i][0], value))
          for i, value in enumerate(row)) for row in cursor.fetchall()]

    print r

    json_output = json.dumps(r)
    return json_output
