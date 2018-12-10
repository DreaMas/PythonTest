from customers import Customers
from transaction_type import TransactionType

from sqlalchemy import Column, String, Integer, Numeric, ForeignKey, Sequence, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Transactions(Base):
    __tablename__ = 'transactions'

    id = Column(Integer, Sequence('transactions_id_seq'), primary_key=True)
    sequential_number = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey(Customers.id), nullable=False)
    timestamp = Column(DateTime(timezone=False))
    type_code = Column(Integer, ForeignKey(TransactionType.id), nullable=False)
    name = Column(String, nullable=True)
    amount = Column(Numeric(19, 2), nullable=False)

    def __init__(self, sequential_number, customer_id, timestamp, type_code, name, amount):
        self.customer_id = customer_id
        self.sequential_number = sequential_number
        self.timestamp = timestamp
        self.type_code = type_code
        self.name = name
        self.amount = amount
