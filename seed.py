# seed.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Restaurant, Customer, Review

# Create a database engine and session
engine = create_engine('sqlite:///restaurant_reviews.db')
Session = sessionmaker(bind=engine)
session = Session()

# Add seed data
restaurant1 = Restaurant(name='Restaurant 1', price=3)
restaurant2 = Restaurant(name='Restaurant 2', price=2)
restaurant3 = Restaurant(name='Restaurant 3', price=4)

customer1 = Customer(first_name='John', last_name='Doe')
customer2 = Customer(first_name='Jane', last_name='Smith')
customer3 = Customer(first_name='Mike', last_name='Johnson')

review1 = Review(star_rating=4, restaurant=restaurant1, customer=customer1)
review2 = Review(star_rating=5, restaurant=restaurant2, customer=customer1)
review3 = Review(star_rating=3, restaurant=restaurant3, customer=customer2)
review4 = Review(star_rating=2, restaurant=restaurant1, customer=customer3)

session.add_all([restaurant1, restaurant2, restaurant3, customer1, customer2, customer3, review1, review2, review3, review4])
session.commit()


