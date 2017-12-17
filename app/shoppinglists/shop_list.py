from app import db
from flask import Blueprint, request, make_response, jsonify
from app.models import ShoppingList
from app.authenticate.token import token_required
import re
from app.v1_helper_functions import response, get_response

shop_list = Blueprint('shop_list', __name__)


@shop_list.route('/v1/shoppinglist/', methods=['POST'])
@token_required
def add_shoppinglists(current_user):
    """"
    Method to create a shopping list
    """
    if request.content_type == 'application/json':

        data = request.get_json()
        name = data.get('name')
        description = data.get('description')

        if name and description:
            if re.match("^([a-zA-Z0-9]+[_-])*[a-zA-Z0-9]+$", name):
                shoplist = ShoppingList(name=name, description=description, user_id=current_user.id)
                db.session.add(shoplist)
                db.session.commit()
                return make_response(jsonify({
                    'id': shoplist.id,
                    'name': shoplist.name,
                    'description': shoplist.description,
                    'user_id': current_user.id,
                    'created_on': shoplist.created_on,
                    'message': 'Shopping list has been created'
                })), 201
            return response('failed', 'Wrong name format. Name can only contain letters and numbers', 400)

        return response('failed', 'No name or description input. Try again', 406)

    return response('failed', 'Content-type must be json', 202)


@shop_list.route('/v1/shoppinglist/', methods=['GET'])
@token_required
def view_shoppinglists(current_user):
    """"
    Method to view all shopping lists belonging to the specified user
    User can limit the number of results returned and can also do a search on all their lists
    """

    limit = request.args.get('limit', 10)
    q = request.args.get('q', None)
    page = int(request.args.get('page', 1))

    results = []
    shoplists = ShoppingList.query.filter_by(
        user_id=current_user.id)

    if q is not None:
        shoplists = shoplists.filter(
            ShoppingList.name.like("%" + q.strip() + "%"))

    if limit:
        try:
            if int(limit):
                shoplists = shoplists.filter_by(
                    user_id=current_user.id).paginate(page=page,
                                                      per_page=int(
                                                          limit), error_out=False).items

                for shoplist in shoplists:
                    results.append(shoplist.json())

                if len(results) == 0:
                    return response('failed', 'Shopping list not found', 404)
                return get_response('Shoppinglists', results)

        except ValueError:
            return response('failed', 'Limit should be an integer', 400)

    for shoplist in shoplists.all():
        results.append(shoplist.json())

    if len(results) == 0:
        return response('failed', 'Shopping list not found', 404)
    return get_response('Shoppinglists', results)


@shop_list.route('/v1/shoppinglist/<id>', methods=['GET'])
@token_required
def get_single_list(current_user, id):
    """"
    Method to view a single shopping list
    """
    if request.content_type == 'application/json':
        try:
            int(id)
        except ValueError:
            return response('failed', 'Please provide a valid ShoppingList Id', 400)
        else:
            shoplist = ShoppingList.query.filter_by(user_id=current_user.id, id=id).first()

            if shoplist is not None:
                return make_response(jsonify({
                    'id': shoplist.id,
                    'name': shoplist.name,
                    'description': shoplist.description,
                    'user_id': current_user.id,

                }

                )), 200
            return response('failed', 'Shopping list not found', 404)
    return response('failed', 'Content-type must be json', 202)


@shop_list.route('/v1/shoppinglist/<id>', methods=['PUT'])
@token_required
def edit_single_list(current_user, id):
    """"
    Method to update a single shopping list
    """
    if request.content_type == 'application/json':
        try:
            int(id)
        except ValueError:
            return response('failed', 'Please provide a valid ShoppingList Id', 400)
        else:

            shoplist = ShoppingList.query.filter_by(user_id=current_user.id, id=id).first()
            if shoplist is not None:
                data = request.get_json()
                name = data.get('name')
                description = data.get('description')
                if name and description:
                    if re.match("^([a-zA-Z0-9]+[_-])*[a-zA-Z0-9]+$", name):
                        shoplist.name = name
                        shoplist.description = description
                        db.session.commit()
                        return make_response(jsonify({
                            'name': shoplist.name,
                            'description': shoplist.description,
                            'message': 'Shopping list has been updated'

                        })), 200
                    return response('failed', 'Wrong name format. Name can only contain letters and numbers', 200)
                return response('failed', 'No name input. Try again', 400)
            return response('failed', 'Shopping list does not exist. Please try again', 404)
    return response('failed', 'Content-type must be json', 202)


@shop_list.route('/v1/shoppinglist/<id>', methods=['DELETE'])
@token_required
def delete_single_list(current_user, id):
    """"
    Method to delete a shopping list
    """
    if request.content_type == 'application/json':
        try:
            int(id)
        except ValueError:
            return response('failed', 'Please provide a valid ShoppingList Id', 400)
        else:
            shoplist = ShoppingList.query.filter_by(user_id=current_user.id, id=id).first()
            if shoplist is not None:
                db.session.delete(shoplist)
                db.session.commit()
                return response('success', 'Shopping list has been deleted', 200)
            return response('failed', 'Shopping list not found', 404)
    return response('failed', 'Content-type must be json', 202)
