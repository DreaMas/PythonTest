import datetime

from flask import Flask, jsonify, abort, make_response, request

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

import json

from alchemyEncoder import AlchemyEncoder

from customers import Customers
# from transaction_type import TransactionType
from transactions import Transactions

engine = create_engine("postgresql+psycopg2://postgres:247050@localhost:5432/pythonTest")
Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()

app = Flask(__name__)


# CustomersAPI
@app.route('/payment_notes/api/v1.0/customers', methods=['GET'])
def get_customers():
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
    customer = Customers(first_name=request.json['first_name'],
                         last_name=request.json['last_name'],
                         company=request.json.get('company'))
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


# TransactionsAPI
@app.route('/payment_notes/api/v1.0/transactions', methods=['GET'])
def get_transactions():
    transactions = session.query(Transactions).all()
    return json.dumps(transactions, cls=AlchemyEncoder)


@app.route('/payment_notes/api/v1.0/transactions/<int:transaction_id>', methods=['GET'])
def get_transaction(transaction_id):
    transaction = session.query(Customers).filter_by(id=transaction_id).first()
    if transaction is None:
        abort(404)
    return json.dumps(transaction, cls=AlchemyEncoder)


@app.route('/payment_notes/api/v1.0/transactions', methods=['POST'])
def create_transaction():
    if not request.json or not('customer_id' and 'type_code' and 'amount') in request.json:
        abort(400)
    transaction = Transactions(customer_id=request.json['customer_id'],
                               timestamp=datetime.datetime.utcnow(),
                               type_code=request.json['type_code'],
                               name=request.json.get('name'),
                               amount=request.json['amount'])
    session.add(transaction)
    session.commit()
    return json.dumps(transaction, cls=AlchemyEncoder), 201


@app.route('/payment_notes/api/v1.0/transactions/<int:transaction_id>', methods=['DELETE'])
def delete_transaction(transaction_id):
    transaction = session.query(Transactions).filter_by(id=transaction_id).first()
    if transaction is None:
        abort(404)
    session.delete(transaction)
    session.commit()
    return jsonify({'result': True})


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == '__main__':
    app.run(debug=True)
