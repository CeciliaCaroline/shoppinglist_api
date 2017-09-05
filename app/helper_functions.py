from flask import make_response, jsonify


def response(status, message, code):
    return make_response(jsonify({
        'status': status,
        'message': message})), code


def get_response(title, results):
    return make_response(jsonify({
        title: results,
        'status': 'success'

    })), 200
