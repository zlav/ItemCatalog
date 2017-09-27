
#This page has been over annotated in order to be used for future reference and re learning purposes

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

#Import the base for the database classes
Base = declarative_base()

#New User DB table
class User(Base):
    #Name the New Table
    __tablename__ = 'user'

    #Initiate table columns
    #nullable = False prevents creation without a value
    #primary_key = True sets the unique identifier for this table
    name = Column(String(40), nullable = False)
    email = Column(String(100), nullable = False)
    picture = Column(String(250))
    id = Column(Integer, primary_key = True)

    #Serialize is how the data formats itself to be printed in JSON form
    @property
    def serialize(self):
        """JSON return of User class"""
        return {
            'name'      : self.name,    
            'email'     : self.email,
            'picture'   : self.picture,
            'id'        : self.integer,
        }

class Category(Base):
    __tablename__ = 'category'
   
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    user_id = Column(Integer, ForeignKey(User.id))
    
    @property
    def serialize(self):
       """Return object data in easily serializeable format"""
       return {
           'name'               : self.name,
           'id'                 : self.id,
           'user_id'            : self.user_id,
       }
 
class Item(Base):
    __tablename__ = 'item'

    name = Column(String(80), nullable = False)
    id = Column(Integer, primary_key = True)
    description = Column(String(250))
    price = Column(String(40))
    picture = Column(String(250))
    category_id = Column(Integer, ForeignKey('category.id'))
    user_id = Column(Integer, ForeignKey(User.id))

    @property
    def serialize(self):
       """Return object data in easily serializeable format"""
       return {
            'name'              : self.name,
            'description'       : self.description,
            'id'                : self.id,
            'price'             : self.price,
            'category'          : self.category,
            'picture'           : self.picture,
            'user_id'           : self.user_id,
      }

#Create the new database after running this file
engine = create_engine('sqlite:///shoppingcatalog.db')

Base.metadata.create_all(engine)
