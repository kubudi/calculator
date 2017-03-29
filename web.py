from flask import Flask
# from flask import json
from flask import request
from flask import jsonify

import math
import os


app = Flask(__name__)


class UnsupportedOperation(Exception):
    def __init__(self, op):
        self.op = op


class WrongParameters(Exception):
    pass


def handle(json):
    op = json['operation']
    print("opreation: {}".format(op))

    val1 = json.get('val1')
    val2 = json.get('val2')
    print("val1: {}".format(val1))
    print("val2: {}".format(val2))

    if op == 'plus':
        if val1 and val2:
            return val1 + val2
        else:
            raise WrongParameters()
    elif op == 'minus':
        if val1 and val2:
            return val1 - val2
        else:
            raise WrongParameters()
    elif op == 'times':
        if val1 and val2:
            return val1 * val2
        else:
            raise WrongParameters()
    elif op == 'divide':
        if val1 and val2 is not None:
            return val1 / val2
        else:
            raise WrongParameters()
    elif op == 'factorial':
        if val1:
            return math.factorial(val1)
        else:
            raise WrongParameters()
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


@app.errorhandler(400)
def wrong_params():
    message = {'message': 'Wrong number of parameters provided.'}
    resp = jsonify(message)
    resp.status_code = 400

    return resp


@app.errorhandler(500)
def internal():
    message = {'message': 'Internal server error'}
    resp = jsonify(message)
    resp.status_code = 500

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
        except WrongParameters:
            return wrong_params()
        except Exception:
            return internal()

        print('Result: {}'.format(res))
        return jsonify(res)
    else:
        return "nok"


@app.route("/", methods=['GET'])
def docs():
    ops = {
        'Addition': 'plus',
        'Substraction': 'minus',
        'Multiplication': 'times',
        'Divison': 'divide',
        'Factorial': 'factorial',
    }

    res = {
        'description': "A simple calculator at your service",
        'url': '/calculator',
        'operations': ops,
        'example request': {'operation': 'plus', 'val1': 3, 'val2': 4}
    }
    return jsonify(res)

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
