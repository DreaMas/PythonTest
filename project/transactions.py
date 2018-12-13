from sqlalchemy import Column, String, Integer, Sequence, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Transactions(Base):
    __tablename__ = 'transactions'

    id = Column(Integer, Sequence('transactions_id_seq'), primary_key=True)
    timestamp = Column(DateTime(timezone=False))
    name = Column(String, nullable=True)

    def __init__(self, customer_id, timestamp, name):
        self.customer_id = customer_id
        self.timestamp = timestamp
        self.name = name
