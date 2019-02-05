import json
import bayeslite


def conv_cursor_to_json(cursor):
    d = {}
    print "fetchall:"
    print cursor.fetchall()
    for row in cursor.fetchall():
        print "row:"
        print row
        for i, column in enumerate(row):
            print "desc:"
            print cursor.description[i][0]
            d[cursor.description[i][0]] = column
    print "d:"
    print d
    r = [(dict((cursor.description[i][0], value))
          for i, value in enumerate(row)) for row in cursor.fetchall()]
    print "r:"
    print r

    json_output = json.dumps(r)
    return json_output
