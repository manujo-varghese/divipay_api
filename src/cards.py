from flask import Blueprint,request
import requests
from src.database import Card, db
from flask.json import jsonify
import json
from src.constants.http_status_codes import HTTP_200_OK, HTTP_404_NOT_FOUND

cards = Blueprint("cards",__name__,url_prefix="/api/v1/cards")

@cards.get("/")
def get_cards_api():
    headersAuth = {
    'Authorization': 'Token b3981cb0d43b56310c52283c13f9028c2555a4ec'
    }
    card  = requests.post('https://backend-challenge-api.herokuapp.com/api/cards/',headers = headersAuth)
    card = json.loads(card.text)
    id = card.get('id')
    balance = card.get('balance')
    user_id = card.get('user')
   
    created_card =Card(id=id,balance=balance,user_id=user_id)

    db.session.add(created_card)
    db.session.commit()
    return jsonify(card)

@cards.get("/all")
def get_cards_all():
   
    data = []
    cards =Card.query.filter(Card.id).all()
    for card in cards:
        card_value ={
             'id':card.id,
            "balance": card.balance,
            "user_id":card.user_id,
            "created": card.created,
            "updated": card.updated
        }
        data.append(card_value)
    return jsonify({'data':data}) ,HTTP_200_OK
@cards.get("/<string:id>")
def get_cards(id):

    card = Card.query.filter_by(id=id).first()

    if not card:
        return jsonify({'message': 'Item not found'}), HTTP_404_NOT_FOUND

    return jsonify({
       'id':card.id,
       "balance": card.balance,
       "user_id":card.user_id,
       "created": card.created,
       "updated": card.updated
    }), HTTP_200_OK

@cards.put('/<string:id>')
@cards.patch('/<string:id>')

def editcard(id):

    updated_card = Card.query.filter_by( id=id).first()

    if not updated_card:
        return jsonify({'message': 'Item not found'}), HTTP_404_NOT_FOUND

    balance = request.get_json().get('balance','')

    updated_card.balance = balance

    db.session.commit()

    return jsonify({
        'id':updated_card.id,
        'balance':updated_card.balance,
        'created':updated_card.created,
        'updated':updated_card.updated
    }), HTTP_200_OK
