from app import db
from flask import Blueprint, request, make_response, jsonify
from flask.views import MethodView
from app.models import Shoppinglist
from app.authenticate.token import token_required
import re
from app.helper_functions import response, get_response

shop_list = Blueprint('shop_list', __name__)


@shop_list.route('/shoppinglist/', methods=['POST'])
@token_required
def add_shoppinglists(current_user):
    """"
    Method to create a shopping list
    """
    if request.content_type == 'application/json':

        # Go ahead and handle the request, the user is authenticated
        data = request.get_json()
        name = data.get('name')
        description = data.get('description')

        if name and description:
            if re.match("^([a-zA-Z0-9]+[_-])*[a-zA-Z0-9]+$", name):
                shoplist = Shoppinglist(name=name, description=description, user_id=current_user.id)
                db.session.add(shoplist)
                db.session.commit()
                return make_response(jsonify({
                    'id': shoplist.id,
                    'name': shoplist.name,
                    'description': shoplist.description,
                    'user_id': current_user.id,
                    'message': 'Shopping list has been created'
                })), 201
            return response('failed', 'Wrong name format. Name can only contain letters and numbers', 400)

        return response('failed', 'No name or description input. Try again', 406)

    return response('failed', 'Content-type must be json', 202)


@shop_list.route('/shoppinglist/', methods=['GET'])
@token_required
def view_shoppinglists(current_user):
    """"
    Method to view all shopping lists belonging to the specified user
    User can limit the number of results returned and can also do a search on all their lists
    """

    limit = request.args.get('limit', 10)
    q = request.args.get('q', None)
    page = int(request.args.get('page', 1))

    if q is not None:
        results = []
        shoplists = Shoppinglist.query.filter(
            Shoppinglist.name.like("%" + q.strip() + "%")).filter_by(
            user_id=current_user.id).all()
        if shoplists:
            for shoplist in shoplists:
                results.append(shoplist.json())

            return get_response('Shoppinglists', results)
        return response('failed', 'Shopping list not found', 404)

    elif limit:
        results = []
        try:
            if int(limit):
                limit_list = Shoppinglist.query.filter_by(
                    user_id=current_user.id).paginate(page=page,
                                                      per_page=int(
                                                          limit), error_out=False).items

                if limit_list:
                    for shoplist in limit_list:
                        results.append(shoplist.json())
                    return get_response('Shoppinglists', results)
                return response('failed', 'Shopping list not found', 404)

        except ValueError:
            return response('failed', 'Limit should be an integer', 400)

    else:
        all_shoplists = Shoppinglist.query.filter_by(user_id=current_user.id)
        if all_shoplists:
            results = []
            for shoplist in all_shoplists:
                results.append(shoplist.json())
            return get_response('Shoppinglists', results)
        return response('failed', 'Shopping list not found', 404)


@shop_list.route('/shoppinglist/<id>', methods=['GET'])
@token_required
def get_single_list(current_user, id):
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
        return response('failed', 'Shopping list not found', 404)

    return response('failed', 'Content-type must be json', 202)


@shop_list.route('/shoppinglist/<id>', methods=['PUT'])
@token_required
def edit_single_list(current_user, id):
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


@shop_list.route('/shoppinglist/<id>', methods=['DELETE'])
@token_required
def delete_single_list(current_user, id):
    """"
    Method to delete a shopping list
    """
    if request.content_type == 'application/json':

        shoplist = Shoppinglist.query.filter_by(user_id=current_user.id, id=id).first()
        if shoplist is not None:
            db.session.delete(shoplist)
            db.session.commit()
            return response('success', 'Shopping list has been deleted', 200)
        return response('failed', 'Shopping list not found', 404)
    return response('failed', 'Content-type must be json', 202)
