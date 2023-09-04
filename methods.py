# from model import Restaurant , Review , Customer

# def get_reviews_for_restaurant(restaurant_instance,session):
#     return session.query(Review).filter_by(restaurant_id=restaurant_instance.id).all()


# def get_customers_for_restaurant(restaurant_instance, session):
#     # Query distinct customers who reviewed the restaurant
#     customer_ids = session.query(Review.customer_id).filter_by(restaurant_id=restaurant_instance.id).distinct().all()
#     customer_ids = [customer_id[0] for customer_id in customer_ids]  # Extract the IDs
#     return session.query(Customer).filter(Customer.id.in_(customer_ids)).all()



# def get_reviews_by_customer(customer_instance, session):
#     return session.query(Review).filter_by(customer_id=customer_instance.id).all()

# def get_restaurants_reviewed_by_customer(customer_instance, session):
#     restaurant_ids = session.query(Review.restaurant_id).filter_by(customer_id=customer_instance.id).distinct().all()
#     restaurant_ids = [restaurant_id[0] for restaurant_id in restaurant_ids]  # Extract the IDs
#     return session.query(Restaurant).filter(Restaurant.id.in_(restaurant_ids)).all()