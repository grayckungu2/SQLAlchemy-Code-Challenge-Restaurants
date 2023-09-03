# models.py

# Import necessary modules
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Create a base class for declarative models
Base = declarative_base()

# Define the Restaurant class
class Restaurant(Base):
    __tablename__ = 'restaurants'
   
    # Define columns
    id = Column(Integer, primary_key=True)
    name = Column(String)
    price = Column(Integer)
   
    # Define relationship with Review class
    reviews = relationship('Review', back_populates='restaurant')
   
    # Define a method to get the customers of the restaurant
    def customers(self):
        return [review.customer for review in self.reviews]
   
    # Define a class method to get the fanciest restaurant
    @classmethod
    def fanciest(cls):
        return session.query(cls).order_by(cls.price.desc()).first()
   
    # Define a method to get all reviews of the restaurant
    def all_reviews(self):
        return [review.full_review() for review in self.reviews]

# Define the Customer class
class Customer(Base):
    __tablename__ = 'customers'
   
    # Define columns
    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
   
    # Define relationship with Review class
    reviews = relationship('Review', back_populates='customer')
   
    # Define a method to get the full name of the customer
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
   
    # Define a method to get the favorite restaurant of the customer
    def favorite_restaurant(self):
        try:
            highest_rating = session.query(Review.star_rating).filter(Review.customer_id == self.id).order_by(Review.star_rating.desc()).first()
            highest_rating_restaurant = session.query(Restaurant).filter(Restaurant.reviews.any(Review.star_rating == highest_rating[0])).first()
            return highest_rating_restaurant
        except NoResultFound:
            return None
   
    # Define a method to add a review for the customer
    def add_review(self, restaurant, rating):
        new_review = Review(customer=self, restaurant=restaurant, star_rating=rating)
        session.add(new_review)
        session.commit()
   
    # Define a method to delete reviews for the customer
    def delete_reviews(self, restaurant):
        reviews_to_delete = session.query(Review).filter(Review.customer_id == self.id, Review.restaurant_id == restaurant.id).all()
        for review in reviews_to_delete:
            session.delete(review)
        session.commit()

# Define the Review class
class Review(Base):
    __tablename__ = 'reviews'
   
    # Define columns
    id = Column(Integer, primary_key=True)
    star_rating = Column(Integer)
   
    # Define relationship with Restaurant and Customer classes
    restaurant_id = Column(Integer, ForeignKey('restaurants.id'))
    restaurant = relationship('Restaurant', back_populates='reviews')
    customer_id = Column(Integer, ForeignKey('customers.id'))
    customer = relationship('Customer', back_populates='reviews')
   
    # Define a method to get the full review
    def full_review(self):
        return f"Review for {self.restaurant.name} by {self.customer.full_name()}: {self.star_rating} stars"

# Create a database engine and session
engine = create_engine('sqlite:///restaurant_reviews.db')
Session = sessionmaker(bind=engine)
session = Session()

# Create tables in the database
Base.metadata.create_all(engine)