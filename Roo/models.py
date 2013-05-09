from sqlalchemy import Table, Column, Integer, String, ForeignKey, Boolean, Float, Date
from sqlalchemy.orm import relationship, backref
from Roo.database import Base

# create a many to many relationship between user and bag
association_table = Table('association', Base.metadata, Column('users_id', Integer, ForeignKey('users.id')), Column('bags_id', Integer, ForeignKey('bags.id')))

class Bag(Base):
  __tablename__ = 'bags'
  id = Column(Integer, primary_key=True)
  store = Column(String(30), unique=True)
  threshold = Column(Float, unique=False)
  amountinbag = Column(Float, unique=False)
  network = Column(String(30), unique=False)
  url = Column(String(200), unique=False)

  def __init__(self, store=None, threshold=None, amountinbag=None, network=None, url=None):
    self.store = store
    self.threshold = threshold
    self.amountinbag = amountinbag
    self.network = network
    self.url = url

  def __repr__(self):
    return '<Bag %r>' % (self.store)

class User(Base):
  __tablename__ = 'users'
  id = Column(Integer, primary_key=True)
  firstname = Column(String(30), unique=False)
  lastname = Column(String(30), unique=False)
  email = Column(String(40), unique=True)
#  address = Column(String(80), unique=False)
  mailbox = Column(Integer, unique=False) #should technically be true but worried itll mad break before we do a lot of error handling
  isauthenticated = Column(Boolean, unique=False)
  bag_id = Column(Integer, ForeignKey('bags.id'))

  bag = relationship("Bag", secondary=association_table, backref=backref('users', order_by=id))


  def __init__(self, firstname=None, lastname=None, email=None, mailbox=None, isauthenticated=None):
    self.firstname = firstname
    self.lastname = lastname
    self.email = email
#    self.address = address
    self.mailbox = mailbox
    self.isauthenticated = False

  def __repr__(self):
    return '<User %r>' % (self.firstname)

class Order(Base):
  __tablename__ = 'orders'
  id = Column(Integer, primary_key=True)
  url = Column(String(200), unique=False)
  price = Column(Float, unique=False)
  details = Column(String(200), unique=False)
  ship = Column(Boolean, unique=False)
  paid = Column(Boolean, unique=False)
  datepaid = Column(Date, unique=False)
  dateordered = Column(Date, unique=False)
  datereceived_shipper = Column(Date, unique=False)
  datereceived_buyer = Column(Date, unique=False)

  bag_id = Column(Integer, ForeignKey('bags.id'))
  user_id = Column(Integer, ForeignKey('users.id'))
  
  bag = relationship("Bag", backref=backref("orders", order_by=id))
  user = relationship("User", backref="orders")

  def __init__(self, url=None, price=None, details=None, ship=None, paid=None, datepaid=None, dateordered=None, datereceived_shipper=None, datereceived_buyer=None, bag_id=None, user_id=None):
    self.url = url
    self.price = price
    self.details = details
    self.ship = ship
    self.paid = paid
    self.datepaid = datepaid
    self.dateordered = dateordered
    self.datereceived_shipper = datereceived_shipper
    self.daterecevied_buyer = datereceived_buyer
    self.bag_id = bag_id
    self.user_id = user_id
    
  def __repr__(self):
    return '<Order %r>' % (self.url)
