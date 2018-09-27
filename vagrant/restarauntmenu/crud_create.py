from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind = engine)
session = DBSession()

# To create a new restaurant database:

# newEntry = ClassName(property = "value", ...)
# session.add(newEntry)
# session.commit()

myFirstRestaurant = Restaurant(name = "Pizza Palace")
session.add(myFirstRestaurant)
session.commit()


# to test:
session.query(Restaurant).all()
# returns "[<database_setup.Restaurant object at 0x8fd740c>]"


# To create a new menuitem:
cheesepizza = MenuItem(name = "Cheese Pizza",
                       description = "Made with all natural ingredients and fresh mozzarella",
                       course = "Entree",
                       price = "8.99",
                       restaurant = myFirstRestaurant)
# must point to the foreign key (in this case myFirstRestaurant) not in quotes.
session.add(cheesepizza)
session.commit()

# To read from database:
firstResult = session.query(Restaurant).first()
# firstResult is now a variable that refers to the first row in the database
# sigle row references let you call column references as method names
# such as first()
firstResult.name
# returns u'Pizza Palace'

# session.query(TableName)
items = session.query(MenuItem).all()
for item in items:
    print item.name


# To update data:
# 1. find entry: execute a query to find the data you want to change and store
# it in a variable. - use filter_by()
# 2. Reset Values
# 3. Add to session
# 4. session.commit()

# 1
veggieBurgers = session.query(MenuItem).filter_by(name = 'Veggie Burger')
for veggieBurger in veggieBurgers:
    print veggieBurger.id
    print veggieBurger.price
    print veggieBurger.restaurant.name
    print "/n"

UrbanVeggieBurger = session.query(MenuItem).filter_by(id = 8).one()
# .one() will only return one firstResult instead of a list.

# 2
UrbanVeggieBurger.price = '2.99'

# 3
session.add(UrbanVeggieBurger)
# must match the session variable changed

# 4
session.commit()


# To Delete data:
# 1. Find entry
# 2. session.delete(entry)
# 3. session.commit()

# 1
spinach = session.query(MenuItem).filter_by(name = 'Spinach Ice Cream').one()

# 2
session.delete(spinach)

# 3
session.commit()
