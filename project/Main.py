from datetime import datetime

from flask import Flask, jsonify, abort, make_response, request

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

import json

from alchemyEncoder import AlchemyEncoder

from customers import Customers
from transaction_type import TransactionType
from transactions import Transactions

engine = create_engine("postgresql+psycopg2://postgres:247050@localhost:5432/pythonTest")
Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()

app = Flask(__name__)


# transactions = [
#     {
#         'id': 1,
#         'customer_id': 1,
#         'timestamp': u'',
#         'type_code': 1,
#         'name': u'payment1',
#         'amount': 100
#     },
#     {
#         'id': 2,
#         'customer_id': 1,
#         'timestamp': u'',
#         'type_code': 2,
#         'name': u'payment2',
#         'amount': 50
#     },
#     {
#         'id': 3,
#         'customer_id': 2,
#         'timestamp': '',
#         'type_code': '1',
#         'name': 'payment3',
#         'amount': 100
#     }
#
# ]
#
# transaction_type = [
#     {
#         'id': 1,
#         'name': 'Funds Receipt'
#     },
#     {
#         'id': 2,
#         'name': 'Disbursement'
#     }
# ]


# CustomersAPI
@app.route('/payment_notes/api/v1.0/customers', methods=['GET'])
def get_customers():
    # return jsonify(json_list=[i.serialize for i in session.query(Customers).all()])
    customers = session.query(Customers).all()
    return json.dumps(customers, cls=AlchemyEncoder)


@app.route('/payment_notes/api/v1.0/customers/<int:customer_id>', methods=['GET'])
def get_customer(customer_id):
    customer = session.query(Customers).filter_by(id=customer_id).first()
    if customer is None:
        abort(404)
    return json.dumps(customer, cls=AlchemyEncoder)


@app.route('/payment_notes/api/v1.0/customers', methods=['POST'])
def create_customer():
    if not request.json or not ('first_name' and 'last_name') in request.json:
        abort(400)
    print (request.json['first_name'])
    print (request.json['last_name'])
    print (request.json.get('company', ""))
    customer = Customers(first_name=request.json['first_name'], last_name=request.json['last_name'],
                         company=request.json.get('company', ""))
    session.add(customer)
    session.commit()
    return json.dumps(customer, cls=AlchemyEncoder), 201


@app.route('/payment_notes/api/v1.0/customers/<int:customer_id>', methods=['DELETE'])
def delete_customer(customer_id):
    customer = session.query(Customers).filter_by(id=customer_id).first()
    if customer is None:
        abort(404)
    session.delete(customer)
    session.commit()
    return jsonify({'result': True})








####### START FROM HERE #######
# TransactionsAPI
@app.route('/payment_notes/api/v1.0/transactions', methods=['GET'])
def get_transactions():
    return jsonify({'transactions': transactions})


@app.route('/payment_notes/api/v1.0/transactions/<int:transaction_id>', methods=['GET'])
def get_transaction(transaction_id):
    transaction = filter(lambda t: t['id'] == transaction_id, transactions)
    if len(transaction) == 0:
        abort(404)
    return jsonify({'customer': transaction[0]})


@app.route('/payment_notes/api/v1.0/transactions', methods=['POST'])
def create_transaction():
    if not request.json or not ('customer_id' and 'type_code' and 'amount') in request.json:
        abort(400)
    transaction = {
        'id': transactions[-1]['id'] + 1,
        'customer_id': request.json['customer_id'],
        'timestamp': datetime.now(),
        'type_code': request.json['type_code'],
        'amount': request.json['amount']
    }
    transactions.append(transaction)
    return jsonify({'transaction': transaction}), 201


@app.route('/payment_notes/api/v1.0/transactions/<int:transaction_id>', methods=['DELETE'])
def delete_transaction(transaction_id):
    transaction = filter(lambda t: t['id'] == transaction_id, transactions)
    if len(transaction) == 0:
        abort(404)
    transactions.remove(transaction[0])
    return jsonify({'result': True})


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == '__main__':
    app.run(debug=True)
