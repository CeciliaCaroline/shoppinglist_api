from app import db
from flask import Blueprint, request, make_response, jsonify
from app.models import Shoppinglist
from app.authenticate.token import token_required
import re
from app.v2_helper_functions import response, get_response

v2_shop_list = Blueprint('v2_shop_list', __name__)


@v2_shop_list.route('/v2/shoppinglist/', methods=['POST'])
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
            if re.match("^([a-zA-Z0-9]+[ \s])*[a-zA-Z0-9]+$", name) and name.strip(' ')[0]:
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
            return response('failed', 'Wrong name format. Name cannot contain special characters or start with a space',
                            400)

        return response('failed', 'No name or description input. Try again', 403)

    return response('failed', 'Content-type must be json', 202)


@v2_shop_list.route('/v2/shoppinglist/', methods=['GET'])
@token_required
def view_shoppinglists(current_user):
    """"
    Method to view all shopping lists belonging to the specified user
    User can limit the number of results returned and can also do a search on all their lists
    """

    limit = request.args.get('limit', 5)
    q = request.args.get('q', None)
    page = int(request.args.get('page', 1))


    results = []
    shoplists = Shoppinglist.query.filter_by(
        user_id=current_user.id)


    if q is not None:
        q = q.lower()
        shoplists = shoplists.filter(
            Shoppinglist.name.like("%" + q.strip() + "%"))


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
                return get_response('Shoppinglists', results, count=Shoppinglist.query.filter_by(
        user_id=current_user.id).count(), page=page, limit=limit)

        except ValueError:
            return response('failed', 'Limit should be an integer', 400)

    for shoplist in shoplists.all():
        results.append(shoplist.json())

    if len(results) == 0:
        print(len(results))
        return response('failed', 'Shopping list not found', 404)
    return get_response('Shoppinglists', results, count=Shoppinglist.query.filter_by(
        user_id=current_user.id).count, page=page, limit=limit)


@v2_shop_list.route('/v2/shoppinglist/<id>', methods=['GET'])
@token_required
def get_single_list(current_user, id):
    """"
    Method to view a single shopping list
    """
    if request.content_type == 'application/json':
        try:
            int(id)
        except ValueError:
            return response('failed', 'Please provide a valid Shoppinglist Id', 400)
        else:
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


@v2_shop_list.route('/v2/shoppinglist/<id>', methods=['PUT'])
@token_required
def edit_single_list(current_user, id):
    """"
    Method to update a single shopping list
    """
    if request.content_type == 'application/json':
        try:
            int(id)
        except ValueError:
            return response('failed', 'Please provide a valid Shoppinglist Id', 400)
        else:

            shoplist = Shoppinglist.query.filter_by(user_id=current_user.id, id=id).first()
            if shoplist is not None:
                data = request.get_json()
                name = data.get('name')
                description = data.get('description')
                if name and description:
                    if re.match("^^([a-zA-Z0-9]+[ \s])*[a-zA-Z0-9]+$", name) and name.strip(' ')[0]:
                        shoplist.name = name
                        shoplist.description = description
                        db.session.commit()
                        return make_response(jsonify({
                            'name': shoplist.name,
                            'description': shoplist.description,
                            'message': 'Shopping list has been updated'

                        })), 200
                    return response('failed',
                                    'Wrong name format. Name cannot contain special characters or start with a space',
                                    400)
                return response('failed', 'No name input. Try again', 403)
            return response('failed', 'Shopping list does not exist. Please try again', 404)
    return response('failed', 'Content-type must be json', 202)


@v2_shop_list.route('/v2/shoppinglist/<id>', methods=['DELETE'])
@token_required
def delete_single_list(current_user, id):
    """"
    Method to delete a shopping list
    """
    if request.content_type == 'application/json':
        try:
            int(id)
        except ValueError:
            return response('failed', 'Please provide a valid Shoppinglist Id', 400)
        else:
            shoplist = Shoppinglist.query.filter_by(user_id=current_user.id, id=id).first()
            if shoplist is not None:
                db.session.delete(shoplist)
                db.session.commit()
                return response('success', 'Shopping list has been deleted', 200)
            return response('failed', 'Shopping list not found', 404)
    return response('failed', 'Content-type must be json', 202)


            # decorator used to allow cross origin requests


@v2_shop_list.after_request
def apply_cross_origin_header(response):
    response.headers['Access-Control-Allow-Origin'] = '*'

    response.headers["Access-Control-Allow-Credentials"] = "true"
    response.headers["Access-Control-Allow-Methods"] = " GET,HEAD,OPTIONS," \
                                                       "POST,PUT,DELETE"
    response.headers["Access-Control-Allow-Headers"] = "Access-Control-Allow-" \
                                                       "Headers, Origin,Accept, X-Requested-With, Content-Type, " \
                                                       "Access-Control-Request-Method, Access-Control-Request-Headers," \
                                                       "Access-Control-Allow-Origin, Authorization"

    return response
