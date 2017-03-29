from flask import Flask
# from flask import json
from flask import request
from flask import jsonify

import os


app = Flask(__name__)


class UnsupportedOperation(Exception):
    def __init__(self, op):
        self.op = op


def handle(json):
    op = json['operation']
    print("opreation: {}".format(op))

    val1 = json['val1']
    val2 = json['val2']
    print("val1: {}".format(val1))
    print("val2: {}".format(val2))

    if op == 'plus':
        return val1 + val2
    elif op == 'minus':
        return val1 - val2
    elif op == 'times':
        return val1 * val2
    elif op == 'divide':
        return val1 / val2
    else:
        raise UnsupportedOperation(op)


@app.errorhandler(400)
def unsupported(error=None):
    message = {
            'message': 'Unsupported operation: ' + error.op,
    }
    resp = jsonify(message)
    resp.status_code = 400

    return resp


@app.route("/calculator", methods=['POST'])
def sum():
    json = request.get_json()
    if json:
        res = ''
        try:
            res = handle(json)
        except UnsupportedOperation as e:
            return unsupported(e)
        print(res)
        return jsonify(res)
    else:
        return "nok"

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
