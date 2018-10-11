from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Category, Base, CatalogItem, User

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


# Create dummy user
User1 = User(name="Totally Legit Robot",
             email="Friendly_Robot@Empty_Warehouse.com",
             picture="user_pic_1.jpg")

session.add(User1)
session.commit()


# Catelog Items for Category 1 (Electronics)
category1 = Category(user_id=1, name="Electronics")

session.add(category1)
session.commit()

descriptionLong = '' + 'This wireless headset features two miniature '
descriptionLong += 'faeries that sing, talk, and beat-box with magically '
descriptionLong += 'enhanced accuracy inside the ear buds. Just don\'t '
descriptionLong += 'ask them to play comedy. Sometimes they can\'t help '
descriptionLong += 'but laugh. Have you ever heard someone laugh from '
descriptionLong += 'inside your ear? ouch.'
catalogItem1 = CatalogItem(user_id=1, name="Wireless Headset",
                           description=descriptionLong,
                           price="$59.99", category=category1)

session.add(catalogItem1)
session.commit()

descriptionLong = '' + 'This portal into other realms is protected by a '
descriptionLong += 'clear plastic shield that won\'t let you pass into it. '
descriptionLong += 'Just don\'t press too hard. This particular model '
descriptionLong += 'measures 65\".'
catalogItem2 = CatalogItem(user_id=1, name="Big Screen TV",
                           description=descriptionLong,
                           price="$1,999.95", category=category1)

session.add(catalogItem2)
session.commit()

descriptionLong = '' + 'This is a heavily enchanted gadget that features a '
descriptionLong += 'mix of technology and sorcery. It can project voice, '
descriptionLong += 'images, and data between similar devices through clouds '
descriptionLong += 'of all things.'
catalogItem3 = CatalogItem(user_id=1, name="Android Smart Phone",
                           description=descriptionLong,
                           price="$599.99", category=category1)

session.add(catalogItem3)
session.commit()

descriptionLong = '' + 'Four mechanical dragon-flies carrying a cyclops eye '
descriptionLong += 'are magically linked to an enchanted smart phone through '
descriptionLong += 'the air.'
catalogItem4 = CatalogItem(user_id=1, name="Drone",
                           description=descriptionLong,
                           price="$299.50", category=category1)

session.add(catalogItem4)
session.commit()


# Catelog Items for Category 2 (Kitchen)
category2 = Category(user_id=1, name="Kitchen")

session.add(category2)
session.commit()

descriptionLong = '' + 'Always ready fresh coffee, warms up in seconds, makes '
descriptionLong += 'one cup or a whole pot. IV not included.'
catalogItem1 = CatalogItem(user_id=1, name="Coffee Maker",
                           description=descriptionLong,
                           price="$89.99", category=category2)

session.add(catalogItem1)
session.commit()

descriptionLong = '' + 'Stainless Steel, easy to clean with removable liner, '
descriptionLong += 'built in timer, keep warm setting.'
catalogItem2 = CatalogItem(user_id=1, name="Rice Cooker",
                           description=descriptionLong,
                           price="$29.99", category=category2)

session.add(catalogItem2)
session.commit()

descriptionLong = '' + 'Includes Walnut Stained wood block, 6 steak knifes, '
descriptionLong += 'kitchen shear, knife sharpener, boning knife, peeling '
descriptionLong += 'knife, paring knife, utility knife, serrated utility '
descriptionLong += 'knife, slicing knife, santoku knife, bread knife, and '
descriptionLong += 'chef knife.'
catalogItem3 = CatalogItem(user_id=1, name="18 Piece Knife Set",
                           description=descriptionLong,
                           price="$89.98", category=category2)

session.add(catalogItem3)
session.commit()

catalogItem4 = CatalogItem(user_id=1, name="Cast Iron Skillet",
                           description="12.5 inches, pre-seasoned cast iron.",
                           price="$24.99", category=category2)

session.add(catalogItem4)
session.commit()

descriptionLong = '' + 'This horrifying contraption brutally mutates any '
descriptionLong += 'fruit put into it. Come to think of it, I doubt it would '
descriptionLong += 'be any nicer to anything at all you put in it.'
catalogItem5 = CatalogItem(user_id=1, name="Fruit Samurai",
                           description=descriptionLong,
                           price="$15.95", category=category2)

session.add(catalogItem5)
session.commit()

# Catelog Items for Category 3 (Automotive)
category3 = Category(user_id=1, name="Automotive")

session.add(category3)
session.commit()

descriptionLong = '' + 'One Pair of 3 Ton Jack Stands with Double Pin Safety.'
catalogItem1 = CatalogItem(user_id=1, name="Jack Stand",
                           description=descriptionLong,
                           price="$29.99", category=category3)

session.add(catalogItem1)
session.commit()

descriptionLong = '' + 'Prevent your vehicle from rolling with this pair of '
descriptionLong += 'Wheel Chocks. Made from heavy duty plastic.'
catalogItem2 = CatalogItem(user_id=1, name="Wheel Chocks",
                           description=descriptionLong,
                           price="$6.99", category=category3)

session.add(catalogItem2)
session.commit()

descriptionLong = '' + '20 inch Crossbar provides extra tork. Includes four '
descriptionLong += 'sizes: 19mm, 7/8, 13/16, and 3/4.'
catalogItem3 = CatalogItem(user_id=1, name="4-Way Lug Wrench",
                           description=descriptionLong,
                           price="$20.00", category=category3)

session.add(catalogItem3)
session.commit()

catalogItem4 = CatalogItem(user_id=1, name="5 Quarts of 5W-30 Oil",
                           description="Fully Synthetic. 5W-30 oil. 5 quarts.",
                           price="$18.72", category=category3)

session.add(catalogItem4)
session.commit()

descriptionLong = '' + 'Warning: do not use this in the wrong container. '
descriptionLong += 'Read all labels and manufacture manuals before use. '
descriptionLong += 'Non-refundable.'
catalogItem5 = CatalogItem(user_id=1, name="Headlight Fluid",
                           description=descriptionLong,
                           price="$9.99", category=category3)

session.add(catalogItem5)
session.commit()


# Catelog Items for Category 4 (Garden)
category4 = Category(user_id=1, name="Garden")

session.add(category4)
session.commit()

descriptionLong = '' + 'Momma told me not to play with scissors, but she '
descriptionLong += 'didn\'t say anything about pruning shears! Fair warning: '
descriptionLong += 'avoid using them on AA batteries and fingers. If you want '
descriptionLong += 'to use them on flautas or taquitos, you might want to '
descriptionLong += 'wash them. Do NOT wash them in the clothes washer! Momma '
descriptionLong += 'was VERY upset after that.'
catalogItem1 = CatalogItem(user_id=1, name="Pruning Shears",
                           description=descriptionLong,
                           price="$10.21", category=category4)

session.add(catalogItem1)
session.commit()

descriptionLong = '' + 'This vicious red beast matches the capacity of 200 '
descriptionLong += 'cows at pasture to eat grass. It prefers, and at times '
descriptionLong += 'demands a drink more potent than moonshine - it\'s called '
descriptionLong += 'gasoline. I don\'t much care for the stuff, but to each '
descriptionLong += 'there own.'
catalogItem2 = CatalogItem(user_id=1, name="Lawn Mower",
                           description=descriptionLong,
                           price="$199.99", category=category4)

session.add(catalogItem2)
session.commit()

descriptionLong = '' + '20 pound bag of organic all season lawn food. Ok, '
descriptionLong += 'I\'m not going to lie here. It\'s poop, dirt, and '
descriptionLong += 'anything the pigs wouldn\'t eat left over from the farm. '
descriptionLong += 'Enjoy!'
catalogItem3 = CatalogItem(user_id=1, name="Fertilizer",
                           description=descriptionLong,
                           price="$30.40", category=category4)

session.add(catalogItem3)
session.commit()

descriptionLong = '' + 'Includes carying tote, gloves, plant rope, pruner, '
descriptionLong += 'weeder, trowel, cultivator, transplanter, and weeding '
descriptionLong += 'fork.'
catalogItem4 = CatalogItem(user_id=1, name="Garden Tool Set",
                           description=descriptionLong,
                           price="$22.99", category=category4)

session.add(catalogItem4)
session.commit()

catalogItem5 = CatalogItem(user_id=1, name="Smooth Rock",
                           description="Found on the side of the road.",
                           price="$0.99", category=category4)

session.add(catalogItem5)
session.commit()


# Catelog Items for Category 5 (Sporting Goods)
category5 = Category(user_id=1, name="Sporting Goods")

session.add(category5)
session.commit()

descriptionLong = '' + '50 lb pull, made from the wood of a treant to resist '
descriptionLong += 'warping and provide extra strength and flexibility.'
catalogItem1 = CatalogItem(user_id=1, name="Elvin Long Bow",
                           description=descriptionLong,
                           price="$349.99", category=category5)

session.add(catalogItem1)
session.commit()

descriptionLong = '' + 'Guaranteed to get rid of pesky pixies.'
catalogItem2 = CatalogItem(user_id=1, name="Pixie Poison",
                           description=descriptionLong,
                           price="$39.99", category=category5)

session.add(catalogItem2)
session.commit()

descriptionLong = '' + 'Lightweight chainmail armor that is magically '
descriptionLong += 'impenetrable. It also shimmers in moonlight.'
catalogItem3 = CatalogItem(user_id=1, name="Mithril Armor",
                           description=descriptionLong,
                           price="$9999.00", category=category5)

session.add(catalogItem3)
session.commit()

descriptionLong = '' + 'Provides 10 minutes of invisibility after drinking.'
catalogItem4 = CatalogItem(user_id=1, name="Elixir of Invisibility",
                           description=descriptionLong,
                           price="$49.95", category=category5)

session.add(catalogItem4)
session.commit()


print "Added catalog items!"
