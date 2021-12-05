from flask import Blueprint
import requests
from src.constants.http_status_codes import HTTP_200_OK, HTTP_406_NOT_ACCEPTABLE
from src.database import Transaction, db
from flask.json import jsonify
import json
from .cards import cards
from flasgger import swag_from
transactions = Blueprint("transactions",__name__,url_prefix="/api/v1/transactions")

@transactions.get("/")
@swag_from('./docs/transactions/transactions.yaml')
def get_transactions_api():
    headersAuth = {
    'Authorization': 'Token b3981cb0d43b56310c52283c13f9028c2555a4ec'
    }
    transaction  = requests.get('https://backend-challenge-api.herokuapp.com/api/transaction/',headers = headersAuth)
    transaction = json.loads(transaction.text)
    print(transaction.get('amount'))
    card_id = transaction.get('card')
    amount = transaction.get('amount')
    merchant = transaction.get('merchant')
    merchant_category = transaction.get('merchant_category')
   
    created_transaction =Transaction(card_id = card_id, amount=amount, merchant=merchant, merchant_category=int(merchant_category))
    card = requests.get('http://127.0.0.1:5000/api/v1/cards/7b3b01eb-dbb4-4d69-8c23-bac4d1957caa')
    card = json.loads(card.text)
    print(card.get('balance'))
    if not card:
        return jsonify({
            'error':'Requested transaction card is not exist'
        })
    if amount & card.get('balance'):

        if amount > card.get('balance'):
            return jsonify({
                'error':'Requested transaction amount exceeds card balance'
            })
    card_controls = requests.get('http://127.0.0.1:5000/api/v1/card_controls/card_id/7b3b01eb-dbb4-4d69-8c23-bac4d1957caa')
    card_controls = json.loads(card_controls.text)
    # print(card_controls['data'])
    for card_control in card_controls['data']:
        if merchant == card_control.get('merchant_control'):
            if card_control.get('max_amount') & amount:
                if amount > card_control.get('max_amount'):
                    return jsonify({
                        'error':'Requested transaction amount exceeds card maximum transaction limit'
                    }), HTTP_406_NOT_ACCEPTABLE
            if card_control.get('min_amount') & amount:
                if amount > card_control.get('min_amount'):
                    return jsonify({
                        'error':'Requested transaction amount doesnot satisfy the minimum transaction limit'
                    }), HTTP_406_NOT_ACCEPTABLE
    # update card balance on successful transaction
    updated_balance = card.get('balance') - amount
    card = requests.post('http://127.0.0.1:5000/api/v1/cards/7b3b01eb-dbb4-4d69-8c23-bac4d1957caa',data ={'balance':updated_balance})
    db.session.add(created_transaction)
    db.session.commit()
    return jsonify(card_controls), HTTP_200_OK

