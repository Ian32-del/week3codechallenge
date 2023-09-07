from sqlalchemy import create_engine , Column , Integer , String , ForeignKey ,MetaData ,Table
from sqlalchemy.orm import relationship , sessionmaker 
from sqlalchemy.ext.declarative import declarative_base 

from database import session

Base = declarative_base()

restaurant_customer_association = Table(
    'restaurant_customer_association',
    Base.metadata,
    Column('restaurant_id', Integer, ForeignKey('restaurants.id')),
    Column('customer_id', Integer, ForeignKey('customers.id'))
)



class Restaurant(Base):
    __tablename__ = 'restaurants'
    
    id = Column(Integer, primary_key=True)
    name = Column(String)
    price = Column(Integer)
    
    reviews = relationship('Review', back_populates='restaurant')
    customers = relationship(
        'Customer',
        secondary=restaurant_customer_association,
        back_populates='restaurants'
    )
    
    def __repr__(cls):
        return f'Restaurant: {cls.name}, price: {cls.price}'
    
    def restaurant_reviews(self):
        reviews = self.reviews 
        formatted_reviews = [
            f"Review by {review.customer.full_name()}: {review.star_rating} stars"
            for review in reviews
        ]
        return formatted_reviews

    def restaurant_customers(self):
        return self.customers
    
    @classmethod
    def fanciest(cls):
        print(session.query(cls).order_by(cls.price.desc()).first())
         

    def all_reviews(self):
        return [f"Review for {self.name} by {review.customer.full_name()}: {review.star_rating} stars." for review in self.reviews]


    
class Customer(Base):
    __tablename__ = 'customers'
    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    reviews = relationship('Review', back_populates='customer')
    restaurants = relationship(
        'Restaurant',
        secondary=restaurant_customer_association,
        back_populates='customers'
    )
    
    def __repr__(self):
        return f'Customer: {self.full_name()}'

    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    def customer_reviews(self):
        reviews = self.reviews
        formatted_reviews = [
            f"Review for {review.restaurant.name} by {self.full_name()}: {review.star_rating} stars."
            for review in reviews
        ]
        return formatted_reviews

    def customer_restaurants(self):
        return self.restaurants

    def favorite_restaurant(self):
        return session.query(Restaurant).join(Review).filter(Review.customer_id == self.id).order_by(Review.star_rating.desc()).first()

    def add_review(self, restaurant, rating, review):
        review = Review(customer=self, restaurant=restaurant, star_rating=rating, review=review)
        session.add(review)
        session.commit()

    def delete_reviews(self, restaurant):
        reviews_to_delete = session.query(Review).filter(Review.customer_id == self.id, Review.restaurant_id == restaurant.id).all()
        for review in reviews_to_delete:
            session.delete(review)
        session.commit()

class Review(Base):
    __tablename__ = 'reviews'
    
    id = Column(Integer, primary_key=True)
    review = Column(String)
    star_rating = Column(Integer)
    restaurant_id = Column(Integer, ForeignKey('restaurants.id'))
    customer_id = Column(Integer, ForeignKey('customers.id'))
    
    restaurant = relationship('Restaurant', back_populates='reviews')
    customer = relationship('Customer', back_populates='reviews')
    
    def customer_review(self):
        return self.customer  
 
    def restaurant_review(self):
        return self.restaurant

    def full_review(self):
        return f"Review for {self.restaurant.name} by {self.customer.full_name()}: {self.star_rating} stars."

