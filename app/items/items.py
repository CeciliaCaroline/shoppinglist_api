from app import db
from flask import Blueprint, request, make_response, jsonify
from flask.views import MethodView
from app.models import User, Shoppinglist, Items
import re

items = Blueprint('items', __name__)


class NewItems(MethodView):
    def post(self, list_id):
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
                    price = data.get('price')

                    if re.match("^[a-zA-Z0-9\s]*$", name) and price:
                        item = Items(name=name, price=price, list_id=list_id)
                        db.session.add(item)
                        db.session.commit()
                        response = jsonify({
                            'id': item.id,
                            'name': item.name,
                            'price': item.price,
                            'user_id': user_id,
                            'message': 'Shopping list item has been created'
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

    def get(self, list_id):
        """"
        Method to view all shopping list items belonging to the specified user
        """

        auth_header = request.headers.get('Authorization')
        auth_token = auth_header.split(" ")[1]

        if auth_token:
            # Decode the token and get the User ID
            user_id = User.decode_auth_token(auth_token)
            if not isinstance(user_id, str):
                # GET all the shoplists created by this user
                shoplists = Shoppinglist.query.filter_by(list_id=list_id)

                for shoplist in shoplists:
                    return make_response(jsonify({
                        'id': shoplist.id,
                        'name': shoplist.name,
                        'price': shoplist.price,
                        'user_id': list_id,
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


# Register classes as views
item_view = NewItems.as_view('new_items')

# Add rules for the api Endpoints
items.add_url_rule('/shoppinglist/<list_id>/items', view_func=item_view, methods=['POST', 'GET'])
