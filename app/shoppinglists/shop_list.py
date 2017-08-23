from app import db
from flask import Blueprint, request, make_response, jsonify
from flask.views import MethodView
from app.models import Shoppinglist, User
import re

shop_list = Blueprint('shop_list', __name__)


class ShoppingLists(MethodView):
    def post(self):
        if request.content_type == 'application/json':
            auth_header = request.headers.get('Authorization')
            auth_token = auth_header.split(" ")[1]

            if auth_token:
                # Decode the token and get the User ID
                user_id = User.decode_auth_token(auth_token)
                if not isinstance(user_id, str):
                    # Go ahead and handle the request, the user is authenticated
                    data = request.get_json()
                    name = data.get('name')
                    description = data.get('description')

                    if re.match("^[a-zA-Z0-9\s]*$", name) and description:
                        shoplist = Shoppinglist(name=name, description=description, user_id=user_id)
                        db.session.add(shoplist)
                        db.session.commit()
                        response = jsonify({
                            'id': shoplist.id,
                            'name': shoplist.name,
                            'description': shoplist.description,
                            'user_id': user_id
                        })
                        return make_response(response), 201

                    return make_response(
                        jsonify({'status': 'failed',
                                 'message': 'Wrong name format. Name can only contain letters and numbers'})), 200

                else:
                    # user is not legit, so the payload is an error message
                    message = user_id
                    response = {
                        'message': message
                    }
                    return make_response(jsonify(response)), 401
            return make_response(jsonify({"message": "Token is invalid"}))
        return make_response(
            jsonify({'status': 'failed', 'message': 'Content-type must be json'})), 202

    def get(self):

        auth_header = request.headers.get('Authorization')
        auth_token = auth_header.split(" ")[1]

        if auth_token:
            # Decode the token and get the User ID
            user_id = User.decode_auth_token(auth_token)
            if not isinstance(user_id, str):
                # GET all the shoplists created by this user
                shoplists = Shoppinglist.query.filter_by(user_id=user_id)
                results = []

                for shoplist in shoplists:
                    obj = {
                        'id': shoplist.id,
                        'name': shoplist.name,
                        'description': shoplist.description,
                        'user_id': user_id,
                        'status': 'success'
                    }
                    results.append(obj)

                return make_response(jsonify(results)), 200

            else:
                # user is not legit, so the payload is an error message
                message = user_id
                response = {
                    'message': message
                }
                return make_response(jsonify(response)), 401

        return make_response(jsonify({"message": "Token is invalid"}))


class ListMethods(MethodView):
    def get(self, id):

        auth_header = request.headers.get('Authorization')
        auth_token = auth_header.split(" ")[1]

        if auth_token:
            # Decode the token and get the User ID
            user_id = User.decode_auth_token(auth_token)
            if not isinstance(user_id, str):
                # Get all the shoplists created by this user
                shoplist = Shoppinglist.query.filter_by(user_id=user_id, id=id).first()
                results = []
                if shoplist is not None:
                    obj = {
                        'id': shoplist.id,
                        'name': shoplist.name,
                        'description': shoplist.description,
                        'user_id': user_id,
                        'status': 'success'
                    }

                    results.append(obj)

                return make_response(jsonify(results)), 200

            else:
                # user is not legit, so the payload is an error message
                message = user_id
                response = {
                    'message': message
                }
                return make_response(jsonify(response)), 401

        return make_response(jsonify({"message": "Token is invalid"}))

    def put(self):
        auth_header = request.headers.get('Authorization')
        auth_token = auth_header.split(" ")[1]

        if auth_token:
            # Decode the token and get the User ID
            user_id = User.decode_auth_token(auth_token)
            if not isinstance(user_id, str):
                # Get all the shoplists created by this user
                shoplist = Shoppinglist.query.filter_by(user_id=user_id, id=id).first()

        pass

    def delete(self):
        pass


# Register classes as views
shoppinglist_view = ShoppingLists.as_view('shop_list')
singlelist_view = ListMethods.as_view('single_list')

# Add rules for the api Endpoints
shop_list.add_url_rule('/shoppinglist', view_func=shoppinglist_view, methods=['POST'])
shop_list.add_url_rule('/shoppinglist', view_func=shoppinglist_view, methods=['GET'])
shop_list.add_url_rule('/shoppinglist/<id>', view_func=singlelist_view, methods=['GET', 'PUT', 'DELETE'])
