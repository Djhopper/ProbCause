import json
import bayeslite


def conv_cursor_to_json(cursor):
    r = [(dict((cursor.description[i][0], value))
          for i, value in enumerate(row)) for row in cursor.fetchall()]
    json_output = json.dumps(r)
    return json_output
