from faker import Faker
import random

from sqlalchemy import create_engine 
from sqlalchemy.orm import sessionmaker

from lib.model import review

if __name__ == '__main__':

    engine = create_engine('sqlite:///restaurant_reviews.db')
    Session = sessionmaker(bind=engine)
    session = Session()

    # session.query(Restaurant).delete()
    # session.query(Review).delete()
    # session.query(Customers).delete()

    fake = Faker()
