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

    def reviews (self , session):
        return session.query(Review).filter_by(restaurant_id=self.id).all()
    
    def customers(self,session):
        customer_ids = session.query(Review.customer_id).filter_by(restaurant_id=self.id).distinct().all()
        customer_ids = [customer_id[0] for customer_id in customer_ids]
        return session.query(Customer).filter(Customer.id.in_(customer_ids)).all()
    

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
    

    def customer (self,session):
        return session.query(Customer).filter_by(id=self.customer_id).first()
    
    def restaurant(self,session):
        return session.query(Restaurant).filter_by(id=self.restaurant_id).first()
    

Session = sessionmaker(bind=engine)
session = Session()

your_review_instance = session.query(Review).first()

customer_instance = your_review_instance.customer(session)
restaurant_instance = your_review_instance.restaurant(session)