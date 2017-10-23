from flask import make_response, jsonify


def response(status, message, code):
    """
    Helper function for status responses
    :param status:
    :param message:
    :param code:
    :return:
    """
    return make_response(jsonify({
        'status': status,
        'message': message})), code


def get_response(title, results):
    """
    helper function for get request

    :param title:
    :param results:
    :return:
    """
    return make_response(jsonify({
        title: results,
        'status': 'success'

    })), 200


def user_response(status, message, auth_token, code):
    """
    helper function for user authentication

    :param status:
    :param message:
    :param auth_token:
    :param code:
    :return:
    """
    return make_response(jsonify({
        'status': status,
        'message': message,
        'auth_token': auth_token

    })), code
