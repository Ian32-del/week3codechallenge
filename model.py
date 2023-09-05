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

    def reviews(self, session):
        return session.query(Review).filter_by(restaurant_id=self.id).all()

    def customers(self, session):
        customer_ids = session.query(Review.customer_id).filter_by(restaurant_id=self.id).distinct().all()
        customer_ids = [customer_id[0] for customer_id in customer_ids]  # Extract the IDs
        return session.query(Customer).filter(Customer.id.in_(customer_ids)).all()
    
    @classmethod
    def fanciest(cls, session):
        return session.query(cls).order_by(cls.price.desc()).first()
    
    def all_reviews(self, session):
        reviews = session.query(Review).filter_by(restaurant_id=self.id).all()
        formatted_reviews = []
        for review in reviews:
            formatted_reviews.append(review.full_review(session))
        return formatted_reviews

    
class Customer(Base):
    __tablename__ = 'customers'

    id = Column (Integer , primary_key=True)
    first_name = Column(String(255) , nullable=False)
    last_name = Column(String(255) , nullable=False)

    reviews = relationship('Review', backref='customer')

    def reviews(self , session):
        return session.query(Review).filter_by(customer_id=self.id).all()

    def restaurants (self,session):
        restaurant_ids = (
            session.query(Review.restaurant_id)
            .filter_by(customer_id=self.id)
            .distinct()
            .all()
        )
        restaurant_ids = [restaurant_id[0]for restaurant_id in restaurant_ids]
        return session.query(Restaurant).filter(Restaurant.id.in_(restaurant_ids)).all()
    
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    def favorite_restaurant(self,session):
        highest_rating = 0
        favorite = None
        for review in self.reviews(session):
            if review.star_rating > highest_rating:
                highest_rating = review.star_rating
                favorite = review.restaurant(session)
        return favorite
    def add_review(self,session,restaurant , rating):
        new_review = Review(star_rating=rating, restaurant=restaurant, customer=self)
        session.add(new_review)
        session.commit()

    def delete_reviews(self, session, restaurant):
        session.query(Review).filter_by(customer_id=self.id, restaurant_id=restaurant.id).delete()
        session.commit()



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
    
    def full_review(self, session):
        restaurant_name = self.restaurant(session).name
        customer_name = self.customer(session).full_name()
        return f"Review for {restaurant_name} by {customer_name}: {self.star_rating} stars."

Session = sessionmaker(bind=engine)
session = Session()

your_review_instance = session.query(Review).first()
customer_instance = your_review_instance.customer(session)
restaurant_instance = your_review_instance.restaurant(session)


first_restaurant = session.query(Restaurant).first()
restaurant_reviews = first_restaurant.reviews(session)
restaurant_customers = first_restaurant.customers(session)


your_review_instance = session.query(Review).first()
customer_instance = your_review_instance.customer(session)
restaurant_instance = your_review_instance.restaurant(session)


print("Review Customer:")
print(f"Customer ID: {customer_instance.id}, Name: {customer_instance.first_name} {customer_instance.last_name}")

print("\nReview Restaurant:")
print(f"Restaurant ID: {restaurant_instance.id}, Name: {restaurant_instance.name}")

print("\nRestaurant Reviews:")
for review in restaurant_reviews:
    print(f"Review ID: {review.id}, Star Rating: {review.star_rating}")

print("\nCustomers Who Reviewed the Restaurant:")
for customer in restaurant_customers:
    print(f"Customer ID: {customer.id}, Name: {customer.first_name} {customer.last_name}")