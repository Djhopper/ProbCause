import json
import bayeslite


def conv_cursor_to_json(cursor, true_json=False):
    r = [dict((cursor.description[i][0], value)
              for i, value in enumerate(row)) for row in cursor.fetchall()]

    return json.dumps(r) if true_json else r
