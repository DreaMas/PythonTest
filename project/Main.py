import dictionary
from flask import Flask, jsonify, abort, make_response, request
from sqlalchemy import create_engine, select, inspect
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, joinedload, subqueryload
from alchemyEncoder import AlchemyEncoder
from flask_cors import cross_origin
from flask_sqlalchemy import SQLAlchemy
from itertools import groupby

from customers import Customers
from transaction_type import TransactionType
from transaction_line_items import TransactionLineItems
from transactions import Transactions

import json
import datetime

engine = create_engine("postgresql+psycopg2://postgres:247050@localhost:5432/pythonTest")
Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()

app = Flask(__name__)
db = SQLAlchemy(app)


# @app.route('/', methods=['GET'])
# def home():
# return "<h1>Distant Reading Archive</h1><p>This site is a prototype API for distant reading of science fiction novels.</p>"
# return render_template('')


# CustomersAPI
@cross_origin()
@app.route('/customers', methods=['GET'])
def get_customers():
    customers = session.query(Customers).all()
    return json.dumps(customers, cls=AlchemyEncoder)


@cross_origin()
@app.route('/customers/<int:customer_id>', methods=['GET'])
def get_customer(customer_id):
    customer = session.query(Customers).filter_by(id=customer_id).first()
    if customer is None:
        abort(404)
    return json.dumps(customer, cls=AlchemyEncoder)


@cross_origin()
@app.route('/customers', methods=['POST'])
def create_customer():
    if request.json and (
            'first_name' and 'last_name') in request.json and request.json['first_name'].replace(" ", "") != '' and \
            request.json['last_name'].replace(" ", "") != '':
        customer = Customers(first_name=request.json['first_name'].replace(" ", ""),
                             last_name=request.json['last_name'].replace(" ", ""),
                             company=request.json.get('company'))
        session.add(customer)
        session.commit()
        return json.dumps(customer, cls=AlchemyEncoder), 201
    abort(400)


@cross_origin()
@app.route('/customers/<int:customer_id>', methods=['DELETE'])
def delete_customer(customer_id):
    customer = session.query(Customers).filter_by(id=customer_id).first()
    if customer is None:
        abort(404)
    session.delete(customer)
    session.commit()
    return jsonify({'result': True})


def object_as_dict(obj):
    return {c.key: getattr(obj, c.key)
            for c in inspect(obj).mapper.column_attrs}




class Struct(object):
    def __init__(self, **entries):
        self.__dict__.update(entries)

# TransactionsAPI
@cross_origin()
@app.route('/transactions', methods=['GET'])
def get_transactions():
    transactionLineItems = session.query(Transactions, TransactionLineItems, Customers, TransactionType).join(
        TransactionLineItems).join(Customers).join(TransactionType).all()
    print(transactionLineItems[0][0].__dict__)
    print(transactionLineItems[0][1].__dict__)
    print(transactionLineItems[0][2].__dict__)
    print(transactionLineItems[0][3].__dict__)
    result = [[k, [x[1:] for x in g]] for k, g in groupby(transactionLineItems, key=lambda x: x[0])]
    return json.dumps(result, cls=AlchemyEncoder)


@cross_origin()
@app.route('/transactions/<int:transaction_id>', methods=['GET'])
def get_transaction(transaction_id):
    transaction = session.query(Transactions).filter_by(id=transaction_id).all()
    if not transaction:
        abort(404)
    return json.dumps(transaction, cls=AlchemyEncoder)


@cross_origin()
@app.route('/transactions', methods=['POST'])
def create_transaction():
    if not request.json or not ('customer_id' and 'type_code' and 'amount') in request.json:
        abort(400)
    transaction = Transactions(customer_id=request.json['customer_id'],
                               timestamp=datetime.datetime.utcnow(),
                               type_code=request.json['type_code'],
                               name=request.json.get('name'),
                               amount=request.json['amount'])
    session.add(transaction)
    session.commit()
    return json.dumps(transaction, cls=AlchemyEncoder), 201


@cross_origin()
@app.route('/transactions/<int:transaction_id>', methods=['DELETE'])
def delete_transaction(transaction_id):
    transaction = session.query(Transactions).filter_by(id=transaction_id).all()
    if not transaction:
        abort(404)
    session.delete(transaction)
    session.commit()
    return jsonify({'result': True})


@app.errorhandler(404)
def not_found(error, text='Not found'):
    return make_response(jsonify({'error': text}), 404)


if __name__ == '__main__':
    app.run(port=5002, debug=False)
