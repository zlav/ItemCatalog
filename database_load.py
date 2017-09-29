from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Category, Base, Item, User

engine = create_engine('sqlite:///shoppingcatalog.db')
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
User1 = User(name="Zach", email="zcjlavallee@gmail.com",
             picture='https://pbs.twimg.com/profile_images/2671170543/18debd694829ed78203a5a36dd364160_400x400.png')
session.add(User1)
session.commit()

# Category for Soccer
category1 = Category(user_id=1, name="Soccer")

session.add(category1)
session.commit()

Item1 = Item(user_id=1, name="Soccer Ball", description="Used to play soccer",
                     price="24.99", category_id=category1.id)

session.add(Item1)
session.commit()

Item2 = Item(user_id=1, name="Cleats", description="Shoes",
                     price="120.99", category_id=category1.id)

session.add(Item2)
session.commit()

Item3 = Item(user_id=1, name="Jersey", description="Shirt",
                     price="54.99", category_id=category1.id)

session.add(Item3)
session.commit()

Item4 = Item(user_id=1, name="Whistle", description="Refs whistle",
                     price="5.99", category_id=category1.id)

session.add(Item4)
session.commit()

Item5 = Item(user_id=1, name="Flag", description="Corner Flag",
                     price="11.99", category_id=category1.id)

session.add(Item5)
session.commit()

category2 = Category(user_id=1, name="Basketball")

session.add(category2)
session.commit()

Item6 = Item(user_id=1, name="Basketball", description="Used to play basketball",
                     price="24.99", category_id=category2.id)

session.add(Item6)
session.commit()

Item7 = Item(user_id=1, name="Basketball Shoes", description="Shoes",
                     price="80.99", category_id=category2.id)

session.add(Item7)
session.commit()

Item8 = Item(user_id=1, name="Hoop", description="Hoop for shooting on",
                     price="350.99", category_id=category2.id)

session.add(Item8)
session.commit()

Item9 = Item(user_id=1, name="Whistle", description="For the Ref",
                     price="5.99", category_id=category2.id)

session.add(Item9)
session.commit()

category3 = Category(user_id=1, name="Skiing")

session.add(category3)
session.commit()

Item10 = Item(user_id=1, name="Skis", description="Used to glide down the slope",
                     price="359.99", category_id=category3.id)

session.add(Item10)
session.commit()

Item11 = Item(user_id=1, name="Ski Poles", description="Used for light inclines",
                     price="59.99", category_id=category3.id)

session.add(Item11)
session.commit()

Item12 = Item(user_id=1, name="Ski Boots", description="Used to connect yourself to the skis",
                     price="159.99", category_id=category3.id)

session.add(Item12)
session.commit()

'''
category_json = json.loads("""{
    "all_categories": [
        {
            "name": "Ball",
            "description": "Kicked in soccer",
            "price": "20.99",
        }
    ]
}""")

for e in category_json['all_categories']:
    category_input = Category(name=e['name'],user_id=1, description=['description'], price=['price'], category_id=categoryid)
    session.add(cateogry_input)
    session.commit()
'''

print "added categories and items with users!"
