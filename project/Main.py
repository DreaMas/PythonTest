import datetime
import decimal

from flask import Flask, jsonify, abort, make_response, request
from sqlalchemy import create_engine, select
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from alchemyEncoder import AlchemyEncoder
from flask_cors import CORS, cross_origin

from customers import Customers
from transaction_type import TransactionType
from transactions import Transactions


import json


engine = create_engine("postgresql+psycopg2://postgres:247050@localhost:5432/pythonTest")
Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()

app = Flask(__name__)
CORS(app)

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


# TransactionsAPI
@cross_origin()
@app.route('/transactions', methods=['GET'])
def get_transactions():
    # transactions = session.query(Transactions, Customers, TransactionType).join(Customers).join(TransactionType).all()
    # transactions = session.query(Transactions, Customers.first_name, Customers.last_name, TransactionType.name).join(Customers).join(TransactionType).all()

    res = session.execute('SELECT transactions.*, c2.first_name, c2.last_name, tt.name AS transacion_type_name FROM transactions INNER JOIN customers c2 on transactions.customer_id = c2.id INNER JOIN transaction_type tt on transactions.type_code = tt.id ORDER BY timestamp')

    # object = session.execute('SELECT transactions.*, c2.first_name, c2.last_name, tt.name AS transacion_type_name FROM transactions INNER JOIN customers c2 on transactions.customer_id = c2.id INNER JOIN transaction_type tt on transactions.type_code = tt.id ORDER BY timestamp').filter(Transactions.data['sequential_number'].astext=='required_key').all()

    # res = session.execute(select([Transactions, Customers.first_name, Customers.last_name]))

    return json.dumps([dict(r) for r in res], ensure_ascii=False, default=str)

    # return json.dumps(res, cls=AlchemyEncoder)


@cross_origin()
@app.route('/transactions/<int:transaction_id>', methods=['GET'])
def get_transaction(transaction_id):
    transaction = session.query(Customers).filter_by(id=transaction_id).first()
    if transaction is None:
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
    transaction = session.query(Transactions).filter_by(id=transaction_id).first()
    if transaction is None:
        abort(404)
    session.delete(transaction)
    session.commit()
    return jsonify({'result': True})


@app.errorhandler(404)
def not_found(error, text='Not found'):
    return make_response(jsonify({'error': text}), 404)


if __name__ == '__main__':
    app.run(debug=False)