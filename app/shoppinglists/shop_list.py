from app import db
from flask import Blueprint, request, make_response, jsonify
from flask.views import MethodView
from app.models import Shoppinglist, User
import re

shop_list = Blueprint('shop_list', __name__)


class ShoppingLists(MethodView):
    """"
    Method to create a shopping list and view all the shopping lists for a user
    """

    def post(self):
        """"
        Method to create a shopping list
        """
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
                            'user_id': user_id,
                            'message': 'Shopping list has been created'
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
        """"
        Method to view all shopping lists belonging to the specified user
        """

        auth_header = request.headers.get('Authorization')
        auth_token = auth_header.split(" ")[1]

        if auth_token:
            # Decode the token and get the User ID
            user_id = User.decode_auth_token(auth_token)
            if not isinstance(user_id, str):
                # GET all the shoplists created by this user
                shoplists = Shoppinglist.query.filter_by(user_id=user_id)

                for shoplist in shoplists:
                    return make_response(jsonify({
                        'id': shoplist.id,
                        'name': shoplist.name,
                        'description': shoplist.description,
                        'user_id': user_id,
                        'status': 'success'
                    })), 200

            else:
                # user is not legit, so the payload is an error message
                message = user_id
                response = {
                    'message': message
                }
                return make_response(jsonify(response)), 401

        return make_response(jsonify({"message": "Token is invalid"}))


class ListMethods(MethodView):
    """"
    Method to view, update and delete a single shopping list
    """

    def get(self, id):
        """"
        Method to view a single shopping list
        """
        auth_header = request.headers.get('Authorization')
        auth_token = auth_header.split(" ")[1]

        if auth_token:
            # Decode the token and get the User ID
            user_id = User.decode_auth_token(auth_token)
            if not isinstance(user_id, str):
                # Get one shoplist created by this user
                shoplist = Shoppinglist.query.filter_by(user_id=user_id, id=id).first()

                if shoplist is not None:
                    return make_response(jsonify({
                        'id': shoplist.id,
                        'name': shoplist.name,
                        'description': shoplist.description,
                        'user_id': user_id,
                        'status': 'success'
                    }

                    )), 200

            else:
                # user is not legit, so the payload is an error message
                message = user_id
                response = {
                    'message': message
                }
                return make_response(jsonify(response)), 401

        return make_response(jsonify({"message": "Token is invalid"}))

    def put(self, id):
        """"
        Method to update a single shopping list
        """
        if request.content_type == 'application/json':
            auth_header = request.headers.get('Authorization')
            auth_token = auth_header.split(" ")[1]

            if auth_token:
                # Decode the token and get the User ID
                user_id = User.decode_auth_token(auth_token)
                if not isinstance(user_id, str):
                    # Get one shoplist created by this user
                    shoplist = Shoppinglist.query.filter_by(user_id=user_id, id=id).first()
                    if shoplist is not None:
                        data = request.get_json()
                        name = data.get('name')
                        description = data.get('description')
                        if re.match("^[a-zA-Z0-9\s]*$", name) and description:
                            shoplist.name = name
                            shoplist.description = description
                            db.session.commit()
                            return make_response(jsonify({
                                'name': shoplist.name,
                                'description': shoplist.description,
                                'message': 'Shopping list has been updated'

                            })), 200
                        return make_response(jsonify({
                            'status': 'failed',
                            'message': 'Invalid list name format. Name can only contain letters and numbers'
                        })), 400
                    return make_response(jsonify({
                        'status': 'failed',
                        'message': 'Shopping list does not exist. Please try again'
                    })), 404

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

    def delete(self, id):
        """"
        Method to delete a shopping list
        """
        if request.content_type == 'application/json':
            auth_header = request.headers.get('Authorization')
            auth_token = auth_header.split(" ")[1]

            if auth_token:
                # Decode the token and get the User ID
                user_id = User.decode_auth_token(auth_token)
                if not isinstance(user_id, str):
                    # Get one shoplist created by this user
                    shoplist = Shoppinglist.query.filter_by(user_id=user_id, id=id).first()
                    if shoplist is not None:
                        db.session.delete(shoplist)
                        db.session.commit()
                        return make_response(jsonify({

                            'message': 'Shopping list has been deleted'

                        })), 200
                    return make_response(jsonify({"message": "List not found"})), 404

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


# Register classes as views
shoppinglist_view = ShoppingLists.as_view('shop_list')
list_view = ListMethods.as_view('list_methods')

# Add rules for the api Endpoints
shop_list.add_url_rule('/shoppinglist', view_func=shoppinglist_view, methods=['POST', 'GET'])
shop_list.add_url_rule('/shoppinglist/<id>', view_func=list_view, methods=['GET', 'PUT', 'DELETE'])
