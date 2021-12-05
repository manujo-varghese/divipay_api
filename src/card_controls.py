from flask import Blueprint, request
from src.constants.http_status_codes import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND
from flask.json import jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required
from src.database import CardControl, db
card_controls = Blueprint("card_controls",__name__,url_prefix="/api/v1/card_controls")
from flasgger import swag_from

@card_controls.route('/',methods=['POST','GET'])
@jwt_required()
@swag_from('./docs/card_control/card_control.yaml')
def handle_card_controls():
    current_user = get_jwt_identity()
    if request.method == 'POST':
        card_id = request.get_json().get('card_id','')
        category_control = request.get_json().get('category_control','')
        merchant_control = request.get_json().get('merchant_control','')
        max_amount = request.get_json().get('max_amount','')
        min_amount = request.get_json().get('min_amount','')
        card_control = CardControl(card_id=card_id,category_control=category_control
        ,merchant_control=merchant_control,max_amount=max_amount,min_amount=min_amount)
        db.session.add(card_control)
        db.session.commit()

        return jsonify({
            'id':card_control.id,
            'card_id':card_control.card_id,
            'category_control':card_control.category_control,
            'merchant_control':card_control.merchant_control,
            'max_amount':card_control.max_amount,
            'min_amount':card_control.min_amount,
            'created':card_control.created,
            'updated':card_control.updated
        }), HTTP_201_CREATED
    else:
        if  not request.get_json():
            return jsonify({
                'error':"Car id is required to pass in the request body to fetch related catd_controls"
            }) , HTTP_400_BAD_REQUEST
        card_id = request.get_json().get('card_id','')
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 5, type=int)
        card_controls =CardControl.query.filter_by(
            card_id=card_id
        ).paginate(page=page, per_page=per_page)

        if not card_controls.items:
                return jsonify({
                'error':'There are no related card controls with this card id'
            }),HTTP_404_NOT_FOUND
        data = []
        for card_control in card_controls.items:
            data.append({
            'id':card_control.id,
            'card_id':card_control.card_id,
            'category_control':card_control.category_control,
            'merchant_control':card_control.merchant_control,
            'max_amount':card_control.max_amount,
            'min_amount':card_control.min_amount,
            'created':card_control.created,
            'updated':card_control.updated
        })
        meta = {
            "page": card_controls.page,
            'pages': card_controls.pages,
            'total_count': card_controls.total,
            'prev_page': card_controls.prev_num,
            'next_page': card_controls.next_num,
            'has_next': card_controls.has_next,
            'has_prev': card_controls.has_prev,

        }

        return jsonify({'data':data, 'meta':meta}), HTTP_200_OK


@card_controls.get("/<int:id>")
@jwt_required()
@swag_from('./docs/card_control/card_control_get.yaml')
def get_card_controls(id):
    current_user = get_jwt_identity()

    card_control = CardControl.query.filter_by(id=id).first()

    if not card_control:
        return jsonify({'message': 'Item not found'}), HTTP_404_NOT_FOUND

    return jsonify({
       'id':card_control.id,
        'card_id':card_control.card_id,
        'category_control':card_control.category_control,
        'merchant_control':card_control.merchant_control,
        'max_amount':card_control.max_amount,
        'min_amount':card_control.min_amount,
        'created':card_control.created,
        'updated':card_control.updated
    }), HTTP_200_OK


@card_controls.get("card_id/<string:id>")
def get_card_controls_with_card_id(id):
    card_controls = CardControl.query.filter_by(card_id=id).all()
    data = []
    if not card_controls:
        return jsonify({'message': 'Item not found'}), HTTP_404_NOT_FOUND
    for card_control in card_controls:
         card_value = {
        'id':card_control.id,
        'card_id':card_control.card_id,
        'category_control':card_control.category_control,
        'merchant_control':card_control.merchant_control,
        'max_amount':card_control.max_amount,
        'min_amount':card_control.min_amount,
        'created':card_control.created,
        'updated':card_control.updated
        }
         data.append(card_value)
    return jsonify({'data':data}) ,HTTP_200_OK

@card_controls.delete("/<int:id>")
@jwt_required()
@swag_from('./docs/card_control/card_control_delete.yaml')
def delete_card_control(id):
    current_user = get_jwt_identity()

    card_control = CardControl.query.filter_by(id=id).first()

    if not card_control:
        return jsonify({'message': 'Item not found'}), HTTP_404_NOT_FOUND

    db.session.delete(card_control)
    db.session.commit()

    return jsonify({}), HTTP_204_NO_CONTENT


@card_controls.put('/<int:id>')
@card_controls.patch('/<int:id>')
@jwt_required()
def editcard_control(id):
    current_user = get_jwt_identity()

    card_control = CardControl.query.filter_by( id=id).first()

    if not card_control:
        return jsonify({'message': 'Item not found'}), HTTP_404_NOT_FOUND

    category_control = request.get_json().get('category_control','')
    merchant_control = request.get_json().get('merchant_control','')
    max_amount = request.get_json().get('max_amount','')
    min_amount = request.get_json().get('min_amount','')


    card_control.category_control = category_control
    card_control.merchant_control = merchant_control
    card_control.max_amount = max_amount
    card_control.min_amount = min_amount

    db.session.commit()

    return jsonify({
        'id':card_control.id,
        'card_id':card_control.card_id,
        'category_control':card_control.category_control,
        'merchant_control':card_control.merchant_control,
        'max_amount':card_control.max_amount,
        'min_amount':card_control.min_amount,
        'created':card_control.created,
        'updated':card_control.updated
    }), HTTP_200_OK
