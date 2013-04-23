from sqlalchemy import Table, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, backref
from Roo.database import Base

association_table = Table('association', Base.metadata, Column('users_id', Integer, ForeignKey('users.id')), Column('bags_id', Integer, ForeignKey('bags.id')))

class Bag(Base):
  __tablename__ = 'bags'
  id = Column(Integer, primary_key=True)
  store = Column(String(30), unique=False)
  threshold = Column(Integer, unique=False)
  amountinbag = Column(Integer, unique=True)
  network = Column(String(30), unique=False)
  item = relationship("Item", backref="bags")

  def __init__(self, store=None, threshold=None, amountinbag=None, network=None):
    self.store = store
    self.threshold = threshold
    self.amountinbag = amountinbag
    self.network = network

  def __repr__(self):
    return '<Bag %r>' % (self.store)

class User(Base):
  __tablename__ = 'users'
  id = Column(Integer, primary_key=True)
  firstname = Column(String(30), unique=False)
  lastname = Column(String(30), unique=False)
  email = Column(String(40), unique=True)
  password = Column(String(40), unique=False)
  address = Column(String(80), unique=False)
  bag_id = Column(Integer, ForeignKey('bags.id'))

  bag = relationship("Bag", secondary=association_table, backref=backref('users', order_by=id))

  def __init__(self, firstname=None, lastname=None, email=None, password=None, address=None, bag_id=None):
    self.firstname = firstname
    self.lastname = lastname
    self.email = email
    self.password = password
    self.address = address

  def __repr__(self):
    return '<User %r>' % (self.firstname)

class Item(Base):
  __tablename__ = 'items'
  id = Column(Integer, primary_key=True)
  url = Column(String(100), unique=False)
  price = Column(Integer, unique=False)
  bag_id = Column(Integer, ForeignKey('bags.id'))
  
  def __init__(self, url=None, price=None, bag_id=None):
    self.url = url
    self.price = price
    
  def __repr__(self):
    return '<Item %r>' % (self.url)
