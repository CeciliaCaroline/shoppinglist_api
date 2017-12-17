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


def del_response(status, message, count, code):
    """

    Helper function for status responses

    :param status:
    :param message:
    :param code:
    :return:
    """
    return make_response(jsonify({

        'status': status,
        'message': message,
        'count': count
    })), code


def get_search_response(title, results, page, limit, search_count, name=None):
    """
     helper function for get request

    :param title:
    :param results:
    :param page:
    :param limit:
    :param search_count:
    :return:
    """
    return make_response(jsonify({
        title: results,
        'status': 'success',
        'page': page,
        'limit': limit,
        'search_count': search_count,
        'name': name

    })), 200


def get_response(title, results, page, limit, count, name=None):
    """
     helper function for get request

    :param title:
    :param results:
    :param page:
    :param limit:
    :param count:
    :return:
    """
    return make_response(jsonify({
        title: results,
        'status': 'success',
        'page': page,
        'limit': limit,
        'count': count,
        'name': name

    })), 200
