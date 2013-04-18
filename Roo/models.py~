from sqlalchemy import Table, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, backref
from Roo.database import Base

#association table
bag_users = Table('bag_users', Base.metadata,
                  Column('bag_id', Integer, ForeignKey('bags.id')), 
                  Column('user_id', Integer, ForeignKey('users.id'))
                  )

class Bag(Base):
  __tablename__ = 'bags'
  id = Column(Integer, primary_key=True)
  store = Column(String(30), unique=False)
  threshold = Column(Integer, unique=False)
  amountinbag = Column(Integer, unique=True)
  network = Column(String(30), unique=False)

  #many to many Bag<-->User
  users = relationship('User', secondary=bag_users, backref='users')
  
  def __init__(self, store=None, threshold=None, amountinbag=None, network=None):
    self.store = store
    self.threshold = threshold
    self.amountinbag = amountinbag
    self.network = network

  def __repr__(self):
    '<Bag %r>' % (self.store)

class User(Base):
  __tablename__ = 'users'
  id = Column(Integer, primary_key=True)
  firstname = Column(String(30), unique=False)
  lastname = Column(String(30), unique=False)
  email = Column(String(40), unique=True)
  address = Column(String(80), unique=False)
  
  def __init__(self, firstname=None, lastname=None, email=None, address=None):
    self.firstname = firstname
    self.lastname = lastname
    self.email = email
    self.address = address

  def __repr__(self):
    '<User %r>' % (self.firstname)

