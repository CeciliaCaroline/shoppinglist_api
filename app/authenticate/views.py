from app import db, bcrypt
from flask import Blueprint, request, make_response, jsonify
from flask.views import MethodView
from app.models import User, BlackListToken
from app.helper_functions import response, user_response
import re

auth = Blueprint('auth', __name__)


class RegisterUser(MethodView):
    """
    View function to register a user via the api
    """

    def post(self):
        if request.content_type == 'application/json':
            post_data = request.get_json()
            email = post_data.get('email')
            password = post_data.get('password')
            if re.match(r"[^@]+@[^@]+\.[^@]+", email) and len(password) > 4:
                user = User.query.filter_by(email=email).first()
                if not user:
                    user = User(email=email, password=password)
                    db.session.add(user)
                    db.session.commit()
                    auth_token = user.encode_auth_token(user_id=user.id)
                    return user_response('success', 'Successfully registered', auth_token.decode("utf-8"), 201)

                return response('failed', 'User already exists, Please sign In', 406)
            return response('failed', 'Missing or wrong email format or password is less than four characters', 400)
        return response('failed', 'Content-type must be json', 202)


class LoginUser(MethodView):
    """"
    View function to log in user
    """

    def post(self):
        if request.content_type == 'application/json':
            post_data = request.get_json()
            email = post_data.get('email')
            password = post_data.get('password')
            if re.match(r"[^@]+@[^@]+\.[^@]+", email) and len(password) > 4:
                user = User.query.filter_by(email=email).first()
                if user and bcrypt.check_password_hash(user.password, password):
                    auth_token = user.encode_auth_token(user.id)
                    return user_response('success', 'Successfully registered', auth_token.decode(), 200)

                return response('failed', 'User does not exist or password is incorrect', 406)
            return response('failed', 'Missing or wrong email format or password is less than four characters', 400)
        return response('failed', 'Content-type must be json', 202)


class LogOutUser(MethodView):
    """"
    Method to log out user
    """

    def post(self):
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


class Reset(MethodView):
    """
    Method to reset user password
    """

    def post(self):
        if request.content_type == 'application/json':
            post_data = request.get_json()
            email = post_data.get('email')
            new_password = post_data.get('newpassword')
            confirm_password = post_data.get('confirmpassword')
            if re.match(r"[^@]+@[^@]+\.[^@]+", email) and len(new_password) > 4:
                user = User.query.filter_by(email=email).first()
                if user:
                    if new_password == confirm_password:
                        user.password = new_password
                        db.session.commit()
                        return response('success', 'Password has been reset', 200)
                    return response('failed', 'Password confirm does not match password. Please try again', 400)
                return response('failed', 'User does not exist. Please login or register', 404)

            return response('failed', 'Missing or wrong email format or password is less than four characters', 406)
        return response('failed', 'Content-type must be json', 202)


# Register classes as views
registration_view = RegisterUser.as_view('register')
login_view = LoginUser.as_view('login')
logout_view = LogOutUser.as_view('logout')
reset_view = Reset.as_view('reset')

# Add rules for the api Endpoints
auth.add_url_rule('/auth/register', view_func=registration_view, methods=['POST'])
auth.add_url_rule('/auth/login', view_func=login_view, methods=['POST'])
auth.add_url_rule('/auth/logout', view_func=logout_view, methods=['POST'])
auth.add_url_rule('/auth/reset_password', view_func=reset_view, methods=['POST'])
