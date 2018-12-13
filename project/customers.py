from sqlalchemy import Column, String, Integer, Sequence, Numeric
from sqlalchemy.ext.declarative import declarative_base
from marshmallow import Schema, fields

Base = declarative_base()


class Customers(Base):
    __tablename__ = 'customers'

    id = Column(Integer, Sequence('customer_id_seq'), primary_key=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    company = Column(String, nullable=True)
    amount = Column(Numeric(19, 2), nullable=True, default=0.00)


    def __init__(self, first_name, last_name, company):
        self.first_name = first_name
        self.last_name = last_name
        self.company = company


# class CustomersSchema(Schema):
#     id = fields.Int(dump_only=True)
#     first_name = fields.Str()
#     last_name = fields.Str()
#     company = fields.Str()
#     amount = fields.Decimal()
#     formatted_name = fields.Method('format_name', dump_only=True)
#
#     def format_name(self, customer):
#         return '{}, {}'.format(customer.first_name, customer.last_name)
