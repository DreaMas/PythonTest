from sqlalchemy import Column, String, Integer, func, Numeric, ForeignKey, Date
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Transactions(Base):
    __tablename__ = 'transactions'

    id = Column(Integer, primary_key=True, nullable=False)
    customer_id = Column(Integer, ForeignKey('cusstomers.id'), nullable=False)
    timestamp = Column(Date, default=func.now(), nullable=False),
    type_code = Column(Integer, ForeignKey('transaction_type.id'), nullable=False),
    name = Column(String(60), nullable=False),
    amount = Column(Numeric(19, 2), nullable=False),