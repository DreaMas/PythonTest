from sqlalchemy import Column, String, Integer, Sequence
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class Customers(Base):
    __tablename__ = 'customers'

    id = Column(Integer, Sequence('customer_id_seq'), primary_key=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    company = Column(String, nullable=True)

    def __init__(self, first_name, last_name, company):
        self.first_name = first_name
        self.last_name = last_name
        self.company = company
