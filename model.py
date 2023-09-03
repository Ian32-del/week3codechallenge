from sqlalchemy import create_engine , Column , Integer , String , ForeignKey
from sqlalchemy.orm import relationship , sessionmaker 
from sqlalchemy.ext.declarative import declarative_base 

engine = create_engine ('sqlite:///restaurant_reviews.db')

Base = declarative_base()

class Restaurant(Base):
    __tablename__ = 'restaurants'


    id = Column (Integer , primary_key = True)
    name = Column (String(255) , nullable=False)
    price = Column(Integer)

    reviews = relationship('Review ' , bankref='restaurant')

class Customer(Base):
    __tablename__ = 'customers'

    id = Column (Integer , primary_key=True)
    first_name = Column(String(255) , nullable=False)
    last_name = Column(String(255) , nullable=False)

    reviews = relationship('Review', bankref='customer')


class Review(Base):
    __tablename__ = 'reviews'

    id = Column (Integer , primary_key = True)
    star_rating = Column(Integer)


    restaurant_id = Column(Integer , ForeignKey('restaurants.id') , nullable=False)
    customer_id = Column(Integer , ForeignKey('customers.id') , nullable=False)