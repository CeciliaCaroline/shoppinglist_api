from app import db
from flask import Blueprint, request, make_response, jsonify
from flask.views import MethodView
from app.models import User, Shoppinglist, Items
from app.authenticate.token import token_required
import re

items = Blueprint('items', __name__)


class NewItems(MethodView):
    """"
    Method to create and view list items
    """
    decorators = [token_required]

    def post(self, current_user, list_id):
        """"
        Methods to create list items
        """
        if request.content_type == 'application/json':

            # Go ahead and handle the request, the user is authenticated
            data = request.get_json()
            name = data.get('name')
            price = data.get('price')

            if re.match("^[a-zA-Z0-9\s]*$", name) and price:
                item = Items(name=name, price=price, list_id=list_id)
                db.session.add(item)
                db.session.commit()
                response = jsonify({
                    'id': item.list_id,
                    'name': item.name,
                    'price': item.price,
                    'user_id': current_user.id,
                    'list_id': list_id,
                    'message': 'Shopping list item has been created'
                })
                return make_response(response), 201

            return make_response(
                jsonify({'status': 'failed',
                         'message': 'Wrong name format. Name can only contain letters and numbers'})), 200

        return make_response(
            jsonify({'status': 'failed', 'message': 'Content-type must be json'})), 202

    def get(self, current_user, list_id):
        """"
        Method to view all shopping list items belonging to the specified user
        """
        user = User.query.filter_by(id=current_user.id).first()
        shoppinglist = user.shoppinglists.filter_by(id=list_id).first()
        items = Items.query.filter_by(list_id=shoppinglist.id)

        if items:
            results = []
            for item in items:
                results.append(item.json())
            return make_response(jsonify({
                'shoppingList_items': results,
                'status': 'success'

            })), 200

        return make_response(jsonify({'message': 'Items not found'}))


class ItemMethods(MethodView):
    """"
    Method to view, update and delete a  shopping list item
    """
    decorators = [token_required]

    def get(self, current_user, list_id, item_id):
        """"
        Method to view a shopping list item
        """
        user = User.query.filter_by(id=current_user.id).first()
        shoppinglist = user.shoppinglists.filter_by(id=list_id).first()
        item = Items.query.filter_by(list_id=shoppinglist.id, item_id=item_id).first()

        if item is not None:
            return make_response(jsonify({
                'id': item.item_id,
                'name': item.name,
                'price': item.price,
                'user_id': current_user.id,
                'list_id': list_id,
                'status': 'success'
            }

            )), 200
        return make_response(jsonify({
            'message': 'Item not found'
        }))

    def put(self, current_user, list_id, item_id):
        """"
        Method to update a shopping list item
        """
        if request.content_type == 'application/json':
            user = User.query.filter_by(id=current_user.id).first()
            shoppinglist = user.shoppinglists.filter_by(id=list_id).first()
            item = Items.query.filter_by(list_id=shoppinglist.id, item_id=item_id).first()
            if item is not None:
                data = request.get_json()
                name = data.get('name')
                price = data.get('description')
                if name:
                    if re.match("^[a-zA-Z0-9\s]*$", name):
                        item.name = name
                        item.price = price
                        db.session.commit()
                        return make_response(jsonify({
                            'name': item.name,
                            'description': item.price,
                            'user_id': current_user.id,
                            'list_id': list_id,
                            'message': 'Shopping list item has been updated'

                        })), 200
                    return make_response(jsonify({
                        'status': 'failed',
                        'message': 'Invalid list name format. Name can only contain letters and numbers'
                    })), 400
                return make_response(jsonify({
                    'message': 'No input. Try again'
                }))
            return make_response(jsonify({
                'status': 'failed',
                'message': 'Shopping list item does not exist. Please try again'
            })), 404

        return make_response(
            jsonify({'status': 'failed', 'message': 'Content-type must be json'})), 202

    def delete(self, current_user, list_id, item_id):
        """"
        Method to delete a shopping list item
        """
        if request.content_type == 'application/json':
            user = User.query.filter_by(id=current_user.id).first()
            shoppinglist = user.shoppinglists.filter_by(id=list_id).first()
            item = Items.query.filter_by(list_id=list_id, item_id=item_id).first()
            if item is not None:
                db.session.delete(item)
                db.session.commit()
                return make_response(jsonify({

                    'message': 'Shopping list item has been deleted'

                })), 200
            return make_response(jsonify({"message": "Item not found"})), 404

        return make_response(
            jsonify({'status': 'failed', 'message': 'Content-type must be json'})), 202


# Register classes as views
new_item_view = NewItems.as_view('new_items')
items_view = ItemMethods.as_view('items')

# Add rules for the api Endpoints
items.add_url_rule('/shoppinglist/<list_id>/items', view_func=new_item_view, methods=['POST', 'GET'])
items.add_url_rule('/shoppinglist/<list_id>/items/<item_id>', view_func=items_view, methods=['GET', 'PUT', 'DELETE'])
