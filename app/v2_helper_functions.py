from flask import make_response, jsonify
from flask_mail import Message
from app import  mail

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


def get_response(title, results, page, limit, count):
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

    })), 200

def send_email(subject, recipients, text_body, html_body=None):
    msg = Message(subject, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    mail.send(msg)

