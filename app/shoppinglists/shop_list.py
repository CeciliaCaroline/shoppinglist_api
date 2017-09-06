from app import db
from flask import Blueprint, request, make_response, jsonify
from flask.views import MethodView
from app.models import Shoppinglist
from app.authenticate.token import token_required
import re

shop_list = Blueprint('shop_list', __name__)


class ShoppingLists(MethodView):
    """"
    Method to create a shopping list and view all the shopping lists for a user
    """
    decorators = [token_required]

    def post(self, current_user):
        """"
        Method to create a shopping list
        """
        if request.content_type == 'application/json':

            # Go ahead and handle the request, the user is authenticated
            data = request.get_json()
            name = data.get('name')
            description = data.get('description')

            if name and description:
                if re.match("^[a-zA-Z0-9]*$", name):
                    shoplist = Shoppinglist(name=name, description=description, user_id=current_user.id)
                    db.session.add(shoplist)
                    db.session.commit()
                    response = jsonify({
                        'id': shoplist.id,
                        'name': shoplist.name,
                        'description': shoplist.description,
                        'user_id': current_user.id,
                        'message': 'Shopping list has been created'
                    })
                    return make_response(response), 201
                return make_response(
                    jsonify({
                        'status': 'failed',
                        'message': 'Invalid name format. Name can only contain numbers and letters'
                    })
                ), 400

            return make_response(
                jsonify({'status': 'failed',
                         'message': 'No input given. Try again'})), 400

        return make_response(
            jsonify({'status': 'failed', 'message': 'Content-type must be json'})), 202

    def get(self, current_user):
        """"
        Method to view all shopping lists belonging to the specified user
        """
        if request.content_type == 'application/json':
            shoplists = Shoppinglist.query.filter_by(user_id=current_user.id)

            result = []
            for shoplist in shoplists:
                result.append(shoplist.json())

            return make_response(jsonify({
                'shoppingLists': result,
                'status': 'success'
            })), 200

        return make_response(
            jsonify({'status': 'failed', 'message': 'Content-type must be json'})), 202


class ListMethods(MethodView):
    """"
    Method to view, update and delete a single shopping list
    """

    decorators = [token_required]

    def get(self, current_user, id):
        """"
        Method to view a single shopping list
        """
        if request.content_type == 'application/json':
            shoplist = Shoppinglist.query.filter_by(user_id=current_user.id, id=id).first()

            if shoplist is not None:
                return make_response(jsonify({
                    'id': shoplist.id,
                    'name': shoplist.name,
                    'description': shoplist.description,
                    'user_id': current_user.id,
                    'status': 'success'
                }

                )), 200
            return make_response(jsonify({'status': 'failed', 'message': 'Shopping list not found'})), 404
        return make_response(
            jsonify({'status': 'failed', 'message': 'Content-type must be json'})), 401

    def put(self, current_user, id):
        """"
        Method to update a single shopping list
        """
        if request.content_type == 'application/json':

            shoplist = Shoppinglist.query.filter_by(user_id=current_user.id, id=id).first()
            if shoplist is not None:
                data = request.get_json()
                name = data.get('name')
                description = data.get('description')
                if name and description:
                    if re.match("^[a-zA-Z0-9\s]*$", name):
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
                return make_response(jsonify({"message": "No input"})), 404
            return make_response(jsonify({
                'status': 'failed',
                'message': 'Shopping list does not exist. Please try again'
            })), 404

        return make_response(
            jsonify({'status': 'failed', 'message': 'Content-type must be json'})), 202

    def delete(self, current_user, id):
        """"
        Method to delete a shopping list
        """
        if request.content_type == 'application/json':

            shoplist = Shoppinglist.query.filter_by(user_id=current_user.id, id=id).first()
            if shoplist is not None:
                db.session.delete(shoplist)
                db.session.commit()
                return make_response(jsonify({

                    'message': 'Shopping list has been deleted'

                })), 200
            return make_response(jsonify({"message": "List not found"})), 404

        return make_response(
            jsonify({'status': 'failed', 'message': 'Content-type must be json'})), 202  # Register classes as views


shoppinglist_view = ShoppingLists.as_view('shop_list')
singlelist_view = ListMethods.as_view('single_list')

# Add rules for the api Endpoints
shop_list.add_url_rule('/shoppinglist', view_func=shoppinglist_view, methods=['POST', 'GET'])
shop_list.add_url_rule('/shoppinglist/<id>', view_func=singlelist_view, methods=['GET', 'PUT', 'DELETE'])
