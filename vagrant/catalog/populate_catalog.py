from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Category, Base, CatalogItem

engine = create_engine('sqlite:///catalog.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()


# Catelog Items for Category 1 (Electronics)
category1 = Category(name="Electronics")

session.add(category1)
session.commit()


catalogItem1 = CatalogItem(name="Bluetooth Headset", description="wireless headset for calls and music. Blootooth 4.2, range of 30 ft.",
                           price="$49.99", category=category1)

session.add(catalogItem1)
session.commit()

catalogItem2 = CatalogItem(name="65 inch 4K Smart TV", description="WebOS 4.0 with built in Google Assistant, Magic Remote, and SmartThinQ",
                           price="$1,999", category=category1)

session.add(catalogItem2)
session.commit()

catalogItem3 = CatalogItem(name="Android Smart Phone", description="waterproof, 6 inch 4k screen, 64GB internal memory, 4GB RAM, 32 Megapixel backfacing camera, 16 MP front facing camera, fingerprint scanner, Android version 8.0",
                           price="$499", category=category1)

session.add(catalogItem3)
session.commit()

catalogItem4 = CatalogItem(name="Drone", description="Quadrocopter drone with autostabilizing 32 megapixel camera, object tracking, auto hover, follow object, auto return, gps, android, 30 minutes flight time on one charge.",
                           price="$299", category=category1)

session.add(catalogItem4)
session.commit()


# Catelog Items for Category 2 (Kitchen)
category2 = Category(name="Kitchen")

session.add(category2)
session.commit()


catalogItem1 = CatalogItem(name="Coffee Maker", description="Always ready fresh coffee, warms up in seconds, makes one cup or a whole pot.",
                           price="89.99", category=category2)

session.add(catalogItem1)
session.commit()

catalogItem2 = CatalogItem(name="Rice Cooker", description="Stainless Steel, easy to clean with removable liner, built in timer, keep warm setting",
                           price="$29.99", category=category2)

session.add(catalogItem2)
session.commit()

catalogItem3 = CatalogItem(name="18 Piece Knife Set", description="Includes Walnut Stained wood block, 6 steak knifes, kitchen shear, knife sharpener, boning knife, peeling knife, paring knife, utility knife, serrated utility knife, slicing knife, santoku knife, bread knife, and chef knife.",
                           price="$89.98", category=category2)

session.add(catalogItem3)
session.commit()

catalogItem4 = CatalogItem(name="Cast Iron Skillet", description="12.5 inches, pre-seasoned cast iron.",
                           price="$24.99", category=category2)

session.add(catalogItem4)
session.commit()


# Catelog Items for Category 3 (Automotive)
category3 = Category(name="Automotive")

session.add(category3)
session.commit()


catalogItem1 = CatalogItem(name="Jack Stand", description="One Pair of 3 Ton Jack Stands with Double Pin Safety.",
                           price="$29.99", category=category3)

session.add(catalogItem1)
session.commit()

catalogItem2 = CatalogItem(name="Wheel Chocks", description="Prevent your vehicle from rolling with this pair of Wheel Chocks. Made from heavy duty plastic.",
                           price="$6.99", category=category3)

session.add(catalogItem2)
session.commit()

catalogItem3 = CatalogItem(name="4-Way Lug Wrench", description="20 inch Crossbar provides eaxtra tork. Includes four sizes: 19mm, 7/8, 13/16, and 3/4",
                           price="$20.00", category=category3)

session.add(catalogItem3)
session.commit()

catalogItem4 = CatalogItem(name="5 Quarts of 5W-30 Oil", description="Fully Synthetic. 5W-30 oil. 5 quarts.",
                           price="$18.72", category=category3)

session.add(catalogItem4)
session.commit()


# Catelog Items for Category 4 (Garden)
category4 = Category(name="Garden")

session.add(category4)
session.commit()


catalogItem1 = CatalogItem(name="Bypass Pruning Shears", description="Trim Rose Bushes to small branches with these ergonomic pruning shears.",
                           price="$10.21", category=category4)

session.add(catalogItem1)
session.commit()

catalogItem2 = CatalogItem(name="Lawn Mower", description="Adjustable hight, gas powered, push mower with detachable mulch bag..",
                           price="$199.99", category=category4)

session.add(catalogItem2)
session.commit()

catalogItem3 = CatalogItem(name="Fertilizer", description="20 pound bag of organic all season lawn food.",
                           price="$30.40", category=category4)

session.add(catalogItem3)
session.commit()

catalogItem4 = CatalogItem(name="Garden Tool Set", description="Includes carying tote, gloves, plant rope, pruner, weeder, trowel, cultivator, transplanter, and weeding fork.",
                           price="$22.99", category=category4)

session.add(catalogItem4)
session.commit()


print "added catalog items!"
