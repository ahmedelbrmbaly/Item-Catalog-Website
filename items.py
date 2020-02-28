#  Sql required libraries
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
# Import Tables
from database_setup import Category, Items, Base, User

# Make connection with database
engine = create_engine('sqlite:///pcstore.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

# Add User1 to database
User1 = User(name="Ahmed Elbrmbaly", email="ahmed.elbrmbaly@gmail.com",
             picture='https://lh3.googleusercontent.com/-nw31POn9WkQ/XJJfm-Y5EuI/AAAAAAAACzk/cn9j5TTGKVQKBVsvc1qX80QnEKz4r2YXgCEwYBhgL/w140-h139-p/2019-03-20.jpg')
session.add(User1)
session.commit()

# CPU category
category1 = Category(name="Cpu", user_id=1)
session.add(category1)
session.commit()

item1 = Items(user_id=1, name="AMD Ryzen 5 3600 ",
              description="6 (2 logical cores per physical)", price="174.99", category=category1)
session.add(item1)
session.commit()

item2 = Items(user_id=1, name="Intel Core i9-10980XE ",
              description="18 (2 logical cores per physical)", price="979", category=category1)
session.add(item2)
session.commit()

item3 = Items(user_id=1, name="AMD Ryzen Threadripper 3990X ",
              description="64 (2 logical cores per physical)", price="3989.99", category=category1)
session.add(item3)
session.commit()

item4 = Items(user_id=1, name="Intel Xeon W-3275M ",
              description="28 (2 logical cores per physical)	", price="7453", category=category1)
session.add(item4)
session.commit()

item5 = Items(user_id=1, name="AMD Ryzen 9 3950X ",
              description="16 (2 logical cores per physical)	", price="749.99", category=category1)
session.add(item5)
session.commit()

item6 = Items(user_id=1, name="Intel Core i7-9700KF ",
              description="8 (2 logical cores per physical)	", price="359.99", category=category1)
session.add(item6)
session.commit()


# GPU category
category2 = Category(name="GPU", user_id=1)
session.add(category2)
session.commit()

item1 = Items(user_id=1, name="GeForce RTX 2060 SUPER ",
              description="Core Clock: 1407 MHz", price="399.99", category=category2)
session.add(item1)
session.commit()

item2 = Items(user_id=1, name="GeForce RTX 2080 Ti ",
              description="Core Clock: 1350 MHz", price="1099.99", category=category2)
session.add(item2)
session.commit()

item3 = Items(user_id=1, name="GeForce RTX 2070 ",
              description="Core Clock: 1410 MHz", price="399.99", category=category2)
session.add(item3)
session.commit()


# GPU category
category3 = Category(name="RAM", user_id=1)
session.add(category3)
session.commit()

item1 = Items(user_id=1, name="Corsair Vengeance LPX 16 GB ",
              description="DDR4-3000 	2 x 8GB", price="72.98", category=category3)
session.add(item1)
session.commit()

item2 = Items(user_id=1, name="G.Skill Ripjaws V Series 16 GB ",
              description="DDR4-3200  2 x 8GB", price="73.99", category=category3)
session.add(item2)
session.commit()

item3 = Items(user_id=1, name="Kingston HyperX Fury 16 GB ",
              description="	DDR4-3200   2 x 8GB", price="89.77", category=category3)
session.add(item3)
session.commit()
