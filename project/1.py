# from sqlalchemy import create_engine
# from sqlalchemy import Column, String
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import sessionmaker
#
#
# def main():
#     db_string = "postgres://postgres:247050@localhost:5432/pythonTest"
#     db = create_engine(db_string)
#     db.execute("INSERT INTO customers (id, first_name, last_name, company) VALUES (1, 'Doctor Strange', 'Scott Derrickson', '2016')")
#     result_set = db.execute("SELECT * FROM customers")
#     for r in result_set:
#         print(r)
#
# if __name__ == "__main__":
#     main()
from flask.json import jsonify
from sqlalchemy import create_engine, select
from sqlalchemy.dialects.postgresql import json
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.serializer import loads, dumps

from alchemyEncoder import AlchemyEncoder

from customers import Customers
from transaction_type import TransactionType
from transactions import Transactions

engine = create_engine("postgresql+psycopg2://postgres:247050@localhost:5432/pythonTest")

Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()

# Create
customer = Customers(first_name="Derrickson", last_name="Scott Derrickson", company="2016")

# session.add(customer)
# session.commit()

c = session.query(Customers).filter_by(id=39).first()
print(c)

# print json.dumps(c, cls=AlchemyEncoder)


session.close()

# # Read
# customers = session.query(Customers)
# for customer in customers:
#     print(customer.first_name)
#
# # Update
# customer.first_name = "Some2016Film"
# session.commit()

# Delete
# session.delete(customer)
# session.commit()


# class Movie(Base):
#     __tablename__ = 'movies'
#
#     id = Column(Integer, primary_key=True)
#     title = Column(String)
#     release_date = Column(Date)
#     actors = relationship("Actor", secondary=movies_actors_association)
#
#     def __init__(self, title, release_date):
#         self.title = title
#         self.release_date = release_date


# bourne_identity = Movie("The Bourne Identity", date(2002, 10, 11))
