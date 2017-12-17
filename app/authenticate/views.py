import re
from app import db, bcrypt, app, mail, Message
from flask import Blueprint, request
from app.models import User, BlackListToken
from app.v1_helper_functions import response, user_response

auth = Blueprint('auth', __name__)


def send_email(subject, recipients, text_body, html_body=""):
    msg = Message(subject, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    mail.send(msg)


@auth.route('/auth/register', methods=['POST'])
def signup():
    """
    View function to register a user via the api
    """

    if request.content_type == 'application/json':
        post_data = request.get_json()
        username = post_data.get('username')
        email = post_data.get('email')
        password = post_data.get('password')
        confirm_password = post_data.get('confirm_password')

        if re.match(r"[^@]+@[^@]+\.[^@]+", email) and len(password) >= 4 and username:
            if password == confirm_password:
                user = User.query.filter_by(email=email).first()
                if not user:
                    user = User(email=email, password=password, username=username)
                    db.session.add(user)
                    db.session.commit()
                    auth_token = user.encode_auth_token(user_id=user.id)

                    return user_response('success', 'Successfully registered', str(auth_token, "utf-8"), 201)

                return response('failed', 'User already exists, Please sign In', 403)
            return response('failed', 'Password does not match. Please try again', 400)
        return response('failed', 'Missing or wrong email format or password is less than five characters', 400)
    return response('failed', 'Content-type must be json', 202)


@auth.route('/auth/login', methods=['POST'])
def login():
    """"
    View function to log in user
    """

    if request.content_type == 'application/json':
        post_data = request.get_json()
        email = post_data.get('email')
        password = post_data.get('password')
        if re.match(r"[^@]+@[^@]+\.[^@]+", email) and len(password) >= 4:
            user = User.query.filter_by(email=email).first()
            if user and bcrypt.check_password_hash(user.password, password):
                auth_token = user.encode_auth_token(user.id)
                return user_response('success', 'Successfully logged in', auth_token.decode(), 200)

            return response('failed', 'User does not exist or password is incorrect', 403)
        return response('failed', 'Missing or wrong email format or password is less than five characters', 400)
    return response('failed', 'Content-type must be json', 202)


@auth.route('/auth/logout', methods=['POST'])
def logout():
    """"
    Method to log out user
    """

    auth_header = request.headers.get('Authorization')
    if auth_header:
        try:
            auth_token = auth_header.split(" ")[1]
        except IndexError:
            return response('failed', 'Provide a valid auth token', 403)
        else:
            decoded_token_response = User.decode_auth_token(auth_token)
            if not isinstance(decoded_token_response, str):
                blacklist = BlackListToken(auth_token)
                try:
                    db.session.add(blacklist)
                    db.session.commit()
                    return response('success', 'Successfully logged out', 200)
                except Exception as e:
                    return response('failed', e, 400)
            return response('failed', decoded_token_response, 401)
    return response('failed', 'Provide an authorization header', 403)


@auth.route('/auth/reset_password/<token>', methods=['POST'])
def reset(token=None):
    """
    Method to reset user password
    """

    if request.content_type == 'application/json':
        post_data = request.get_json()
        email = post_data.get('email')
        new_password = post_data.get('new_password')
        confirm_password = post_data.get('confirm_password')
        if re.match(r"[^@]+@[^@]+\.[^@]+", email) and len(new_password) > 4:
            user = User.query.filter_by(email=email).first()
            user_id = user.decode_auth_token(token)
            if user_id and user.id == user_id:
                if new_password == confirm_password:
                    user.password = bcrypt.generate_password_hash(new_password, app.config.get('BCRYPT_LOG_ROUNDS')) \
                        .decode('utf-8')
                    db.session.commit()
                    return response('success', 'Password has been reset', 200)
                return response('failed', 'Password confirm does not match password. Please try again', 400)
            return response('failed', 'Invalid user. You cant change your password with this token', 404)

        return response('failed', 'Missing or wrong email format or password is less than four characters', 403)
    return response('failed', 'Content-type must be json', 202)

    # decorator used to allow cross origin requests


@auth.route('/auth/reset_password', methods=['POST'])
def reset_password():
    """
    Method to reset user password
    """
    if request.content_type == 'application/json':
        post_data = request.get_json()
        email = post_data.get('email')
        # retrieve user and check if they exist
        user = User.query.filter_by(email=email).first()

        # user does not exist
        if not user:
            return response('failed', 'User does not exist. Please login or register', 404)
        token = user.encode_auth_token(user.id)

        # user exists, make a token from the secret key and
        # a dictionary of the users email

        # create a url and send it in the email
        password_reset_url = \
            "http://localhost:3000/auth/" \
            "reset_password/" + str(token, 'utf-8')

        email_body = \
            "Please follow this link to reset your " \
            "password\n\n" + password_reset_url + "\n\n If you're " \
                                                  "not the one who requested this, please ignore " \
                                                  "this and contact the administrator about this."

        send_email(
            'Password Reset Requested', [email], email_body)

        # return a success message
        return response("success", "An email has been sent to you with a link you can use to reset your password", 200)
    return response('failed', 'Content-type must be json', 202)


@auth.after_request
def apply_cross_origin_header(response):
    """
    decorator to handle cors
    :param response:
    :return:
    """
    response.headers['Access-Control-Allow-Origin'] = '*'

    response.headers["Access-Control-Allow-Credentials"] = "true"
    response.headers["Access-Control-Allow-Methods"] = "GET,HEAD,OPTIONS," \
                                                       "POST,PUT,DELETE"
    response.headers["Access-Control-Allow-Headers"] = \
        "Access-Control-Allow-" \
        "Headers, Origin,Accept, X-Requested-With, Content-Type, " \
        "Access-Control-Request-Method, Access-Control-Request-Headers," \
        "Access-Control-Allow-Origin, Authorization"

    return response
