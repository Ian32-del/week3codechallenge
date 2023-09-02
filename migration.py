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

    reviews = relationship('Review ' , backref='restaurant')

class Customer(Base):
    __tablename__ = 'customers'

    id = Column (Integer , primary_key=True)
    first_name = Column(String(255) , nullable=False)
    