from sqlalchemy import Column, Integer, Numeric, ForeignKey, Sequence, DateTime
from sqlalchemy.ext.declarative import declarative_base

from transactions import Transactions
from customers import Customers

from transaction_type import TransactionType

Base = declarative_base()


class TransactionLineItems(Base):
    __tablename__ = 'transaction_line_items'

    id = Column(Integer, Sequence('transaction_line_items_id_seq'), primary_key=True)
    transaction_id = Column(Integer, ForeignKey(Transactions.id), nullable=False)
    customer_id = Column(Integer, ForeignKey(Customers.id), nullable=False)
    type_code = Column(Integer, ForeignKey(TransactionType.id), nullable=False)
    amount = Column(Numeric(19, 2), nullable=True, default=0.00)

    def __init__(self, customer_id, amount):
        self.customer_id = customer_id
        # self.timestamp = timestamp
        self.amount = amount
