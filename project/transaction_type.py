from sqlalchemy import Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class TransactionType(Base):
    __tablename__ = 'transaction_type'

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(60), nullable=False)

    def __init__(self, name):
        self.name = name
