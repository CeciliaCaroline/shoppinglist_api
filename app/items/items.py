from app import db
from flask import Blueprint, request, make_response, jsonify
from app.models import User, Items
from app.authenticate.token import token_required
import re
from app.v1_helper_functions import response, get_response

items = Blueprint('items', __name__)


@items.route('/v1/shoppinglist/<list_id>/items/', methods=['POST'])
@token_required
def add_items(current_user, list_id):
    """"
    Methods to create list items
    """
    if request.content_type == 'application/json':
        try:
            int(list_id)
        except ValueError:
            return response('failed', 'Please provide a valid list Id', 400)
        else:

            # Go ahead and handle the request, the user is authenticated
            data = request.get_json()
            name = data.get('name')
            price = data.get('price')

            if name:
                if re.match("^([a-zA-Z0-9]+[_-])*[a-zA-Z0-9]+$", name):
                    try:
                        if int(price):
                            item = Items(name=name, price=price, list_id=list_id)
                            db.session.add(item)
                            db.session.commit()
                            return make_response(jsonify({
                                'id': item.item_id,
                                'name': item.name,
                                'price': item.price,
                                'user_id': current_user.id,
                                'list_id': list_id,
                                'message': 'Shopping list item has been created'

                            })), 201

                    except ValueError:
                        return response('failed', 'Item price should be an integer', 400)

                return response('failed', 'Wrong name format. Name can only contain letters and numbers', 406)
            return response('failed', 'No name has been input', 400)

    return response('failed', 'Content-type must be json', 202)


@items.route('/v1/shoppinglist/<list_id>/items/', methods=['GET'])
@token_required
def view_items(current_user, list_id):
    """"
    Method to view all shopping list items belonging to the specified user
    User can limit results returned and search their lists
    """
    try:
        int(list_id)
    except ValueError:
        return response('failed', 'Please provide a valid list Id', 400)
    else:
        user = User.query.filter_by(id=current_user.id).first()
        shoppinglist = user.shoppinglists.filter_by(id=list_id).first()
        limit = request.args.get('limit', 10)
        q = request.args.get('q', None)
        page = int(request.args.get('page', 1))

        new = []
        shop_items = Items.query.filter_by(list_id=shoppinglist.id)
        if q is not None:
            new = []
            shop_items = shop_items.filter(Items.name.like("%" + q.strip() + "%"))

        if limit:
            try:
                if int(limit):
                    limit_items = shop_items.filter_by(
                        list_id=list_id).paginate(page=page,
                                                  per_page=int(
                                                      limit), error_out=False).items

                    for limit_item in limit_items:
                        new.append(limit_item.json())
                    if len(new) == 0:
                        return response('failed', 'Shopping list item not found', 404)
                    return get_response('Shoppinglists items', new)

            except ValueError:
                return response('failed', 'Limit should be an integer', 400)

            for item in shop_items.all():
                new.append(item.json())
            if len(new) == 0:
                return response('failed', 'Shopping list item not found', 404)
            return get_response('Shoppinglists items', new)


@items.route('/v1/shoppinglist/<list_id>/items/<item_id>', methods=['GET'])
@token_required
def get_single_item(current_user, list_id, item_id):
    """"
    Method to view a shopping list item
    """
    try:
        int(item_id)
        int(list_id)
    except ValueError:
        return response('failed', 'Please provide a valid item or list Id', 400)
    else:
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

            })), 200
        return response('failed', 'Item not found', 404)


@items.route('/v1/shoppinglist/<list_id>/items/<item_id>', methods=['PUT'])
@token_required
def edit_item(current_user, list_id, item_id):
    """"
    Method to update a shopping list item
    """
    if request.content_type == 'application/json':

        try:
            int(item_id)
            int(list_id)
        except ValueError:
            return response('failed', 'Please provide a valid item or list Id', 400)
        else:
            user = User.query.filter_by(id=current_user.id).first()
            shoppinglist = user.shoppinglists.filter_by(id=list_id).first()
            item = Items.query.filter_by(list_id=shoppinglist.id, item_id=item_id).first()
            if item is not None:
                data = request.get_json()
                name = data.get('name')
                price = data.get('price')
                if name:
                    if re.match("^([a-zA-Z0-9]+[_-])*[a-zA-Z0-9]+$", name):
                        try:

                            if int(price):
                                item.name = name
                                item.price = price
                                db.session.commit()

                                return response('success', 'Shopping list item has been edited', 200)

                        except ValueError:
                            return response('failed', 'Item price should be an integer', 400)
                    return response('failed', 'Wrong name format. Name can only contain letters and numbers', 406)
                return response('failed', 'No name input. Try again', 400)
            return response('failed', 'Shopping list item does not exist. Please try again', 404)
    return response('failed', 'Content-type must be json', 202)


@items.route('/v1/shoppinglist/<list_id>/items/<item_id>', methods=['DELETE'])
@token_required
def delete_item(current_user, list_id, item_id):
    """"
    Method to delete a shopping list item
    """
    if request.content_type == 'application/json':
        try:
            int(item_id)
            int(list_id)
        except ValueError:
            return response('failed', 'Please provide a valid item or list Id', 400)
        else:
            user = User.query.filter_by(id=current_user.id).first()
            shoppinglist = user.shoppinglists.filter_by(id=list_id).first()
            item = Items.query.filter_by(list_id=list_id, item_id=item_id).first()
            if item is not None:
                db.session.delete(item)
                db.session.commit()
                return response('success', 'Shopping list item has been deleted', 200)
            return response('failed', 'Item not found', 404)
    return response('failed', 'Content-type must be json', 202)


    # decorator used to allow cross origin requests
    # @items.after_request
    # def apply_cross_origin_header(response):
    #     response.headers['Access-Control-Allow-Origin'] = '*'
    #
    #     response.headers["Access-Control-Allow-Credentials"] = "true"
    #     response.headers["Access-Control-Allow-Methods"] = "GET,HEAD,OPTIONS," \
    #                                                        "POST,PUT,DELETE"
    #     response.headers["Access-Control-Allow-Headers"] = "Access-Control-Allow-" \
    #         "Headers, Origin,Accept, X-Requested-With, Content-Type, " \
    #         "Access-Control-Request-Method, Access-Control-Request-Headers," \
    #         "Access-Control-Allow-Origin, Authorization"
    #
    #     return response
