# import statements
from Roo import app
from Roo.CASClient import CASClient
from Roo.database import db_session
from Roo.models import User, Bag, Order
from flask import Flask, request, session, g, redirect, url_for, \
	abort, render_template, flash
from flask_oauth import OAuth
from flask.ext.mail import Message
from Roo import mail
import time, ast
from werkzeug.wrappers import BaseResponse
from functools import wraps


def with_netid(f):
  @wraps(f)
  def decorated_function(*args, **kwargs):
    C = CASClient()
    netid = C.Authenticate()
    if isinstance(netid, BaseResponse):
      return netid
    return f(netid, *args, **kwargs)
  return decorated_function

@app.errorhandler(401)
def login_first(e):
  return redirect(url_for('fblogin'))


#test modal
@app.route('/modal')
def modal():
  return render_template('modal.html')

# opening page of the site.  
@app.route('/')
def fblogin():
  # if not logged in, redirect to facebook
  if not session.get('logged_in'):
    return render_template('login.html')
  # if already logged in, redirect to home.
  else:
    return redirect(url_for('home'))

# Princeton CAS login authentication.
@app.route('/cas')
@with_netid
def cas(netid):
  user = User.query.filter_by(id = session['userid']).first()
  user.isauthenticated = True
  session['logged_in'] = True
  db_session.commit()
  return redirect(url_for('home'))


# for all these email notifications we keep in the app.route for debugging purposes so that we can email on demand w/o heroku scheduler

# Email notifications to users with orders telling them to pay for their order
# Happens weekly using Heroku Scheduler
@app.route('/payemail')
def payemail():
  # Send emails to purchase bags every Friday ( 12 noon )
  localtime = time.localtime(time.time())
  dayoftheweek = localtime[6]
#  if dayoftheweek == 5:  # 5 = Friday
  if dayoftheweek < 10000:
    bags = Bag.query.all()
    for bag in bags:
      subject = "Milkman order for %s" % bag.store
      if len(bag.users) == 1:
        # send apology message
        msg = Message(recipients=[bag.users[0].email], subject=subject, sender="themilkmanipping@gmail.com")
        msg.html = "Sorry, no one else joined your Milkman crate :(. Just go ahead and order it on your own. Better luck next week!" 
        mail.send(msg)
      msgtext = None
      if bag.amountinbag >= bag.threshold:
        msgtext = "The Milkman has delivered: your crate for %s meets the minimum for free shipping!<br>" % bag.store
      else:
        msgtext = "While your Milkman crate for %s did not meet the minimum for free shipping, you can still save on shipping by ordering together!<br>" % bag.store
      if len(bag.users) > 1:
        bagleader = bag.users[0]
        for order in bag.orders:
          if order.ship == True:
            bagleader = order.user
        recipients = []
        for user in bag.users:
          recipients.append(user.email)
        msg = Message(recipients=recipients, subject=subject, sender="themilkmanshipping@gmail.com")
        msgtext = msgtext + "The crate should be ordered by " + bagleader.firstname + " " + bagleader.lastname + " (" + bagleader.email + ")<br><br> Here are the orders in the crate: <br><hr>"
        for order in bag.orders:
          msgtext = msgtext + "User: " + order.user.firstname + " " + order.user.lastname + " (" + order.user.email + ") " + "Order cost: $" + str(order.price) + " URL: " + order.url
          msgtext = msgtext + "<br> Comments: " + order.details + "<hr>"
        msg.html = msgtext
        mail.send(msg)
#    users = User.query.all()
#    with mail.connect() as conn:
#      for user in users:
#        # if the user actually has orders in the bag
#        if user.orders:
#          subject = "hello, %s, your purchases on The Milkman are ready to be ordered" % user.firstname
#          msg = Message(recipients=[user.email], subject=subject, sender="rooshipping@gmail.com")
          # link to purchase page.
#          msg.html = """<p>Hey there, <br>, Your order(s) are ready to be purchased and shipped!  Head on over to The Milkman using the link below!<br><br><a href="rooprinceton.herokuapp.com/purchase/"""+str(user.id)+""""><b>Get me my stuff!</b></a></p><br><br> The Milkman""" 
#          conn.send(msg)

# Send reminder emails in case a user has not yet paid for their order
# This reminder email should happen 12 hours later ( Saturday midnight )
# Sent via Heroku Scheduler
@app.route('/reminderemail')
def reminderemail():
  localtime = time.localtime(time.time())
  dayoftheweek = localtime[6]
#  if dayoftheweek == 6:
  if dayoftheweek < 10000:
    users = User.query.all()
    with mail.connect() as conn:
      for user in users:
        # if the user has not purchased any of his or her order, send an email
        for order in user.orders:
           if not order.paid:
            subject = "hello, %s, please pay for your order on The Milkman!" % user.firstname
            msg = Message(recipients=[user.email], subject=subject, sender="themilkmanshipping@gmail.com")
            msg.html = """ Hey there, <br> Just a reminder to pay for your orders!  We know you want your stuff as soon as possible!  Click the link below to pay now! <br><br><a href="rooprinceton.herokuapp.com/purchase/"""+str(user.id)+""""><b>Get me my stuff!</b></a><br><br> The Milkman</p>"""
            conn.send(msg)

# Send an email once the purchase has been made
@app.route('/purchasedemail')
def purchasedemail():
  return "hello"

# Send an email once the purchase has been received, per our tracking information
@app.route('/receivedemail')
def receivedemail():
  return "hello"

@app.route('/editorder/<orderid>', methods=['GET', 'POST'])
def editorder(orderid):
  if not session.get('logged_in'):
    abort(401)
  user = User.query.filter_by(id=session.get('userid')).first()
  valid = False
  for order in user.orders:
    if order.id == orderid:
      valid = True
  if not valid:
    return "Hey dickhead, you're not supposed to be here"

  if request.method == 'POST':
    # check the validity of input, if something is wrong, return the page with error messages where appropriate
    errorfound = False
    try:
      price = float(request.form['price'])
      if price < 0:
        flash("Invalid price", "priceerror")
        errorfound = True
    except ValueError:
      flash("Invalid price", "priceerror")
      errorfound = True
    # check if any fields were left empty                                                                                              
    if not request.form['itemurl']:
      flash("Please input the item's URL", "missingurlerror")
      errorfound = True
    if not request.form['price']:
      flash("Please input the price of the item", "missingpriceerror")
      errorfound = True
    if not request.form['details']:
      flash("Please enter details about your order", "missingdetailserror")
      errorfound = True
    if errorfound:
      return "ERROR"

    order = Order.query.filter_by(id=orderid).first()    
    order.bag.amountinbag = order.bag.amountinbag - order.price + float(request.form['price'])
    order.price = float(request.form['price'])
    order.url = request.form['itemurl']
    order.details = request.form['details']
    ship = False
    if 'ship' in request.form:
      ship = True
    order.ship = ship
    db_session.commit()

    flash("Your purchase of " + order.url + " has been updated for the " + order.bag.store + " bag!", "addmessage")
    return render_template('editorder.html', order=order, bag=order.bag)
  else:
    order = Order.query.filter_by(id=orderid).first()
    return render_template('editorder.html', order=order, bag=order.bag)

@app.route('/purchase/<userid>')
def paypal(userid):
  if not sesssion.get('logged_in'):
    abort(401)
  if not session.get('userid') == userid:
    return "Hey, you're not allowed to see this page!"
  # add in a tab to make the user log in if they're not already logged in..
  # need to make sure it redirects to the purchase page.
  user = User.query.filter_by(id=userid).first()
  total = 0.0
  for order in user.orders:
    total = total + order.price
  return render_template('purchase.html', user=user, total=total)

@app.route('/home')
def home():
  if not session.get('logged_in'):
    abort(401)
  # store the bagid's for the featured stores on the carousel
  # urban outfitters
  urbanoutfittersid = Bag.query.filter_by(store = 'Urban Outfitters').first().id
  # ralph lauren
  ralphlaurenid = Bag.query.filter_by(store = 'Ralph Lauren').first().id
  # j. crew
  jcrewid = Bag.query.filter_by(store = 'J. Crew').first().id
  
  address = True

  userid = session.get('userid')
  allbags = Bag.query.all()
  user = User.query.filter_by(id=userid).first()
  mybags = []
  for b in user.bag:
    mybags.append(b)
  return render_template('home.html', userid=userid, urbanoutfittersid=urbanoutfittersid, ralphlaurenid=ralphlaurenid, jcrewid=jcrewid, mybags=mybags, allbags=allbags, address=address)

# about page
@app.route('/about')
def about():
  if not session.get('logged_in'):
    abort(401)
  return render_template('about.html', userid=session.get('userid'))

# my networks 
@app.route('/mynetworks/<userid>')
def mynetworks(userid):
  if not session.get('logged_in'):
    abort(401)
  if not session.get('userid') == userid:
    return "Hey dickhead, you're not supposed to be here"
  return render_template('mynetworks.html', user=User.query.filter_by(id=userid).first())

# all bags
@app.route('/allbags')
def allbags():
  if not session.get('logged_in'):
    abort(401)
  allbags = Bag.query.all()
  return render_template('allbags.html', userid=session.get('userid'))

# a test page for the admin
@app.route('/all')
def all():
  if not session.get('logged_in'):
    abort(401)
  entries = ""
  for row in User.query.all():
    entries = entries + "first name: " + row.firstname + '<br>'
    entries = entries + "last name: " + row.lastname + '<br>'
    entries = entries + "address: " + row.address + '<br>'
    entries = entries + "email: " + row.email + '<br><br>'
    for row2 in row.bag:
      entries = entries + "bags involved: " + str(row2.store) + '<br>'
    for row2 in row.orders:
      entries = entries + "order: " + str(row2.price) + '<br>'
      
  entries = entries + "<br><br><br><br><br>Now, the Bags:<br>"
    
  for row in Bag.query.all():
    entries = entries + "store name: " + row.store + "<br>"
    entries = entries + "threshold: " + str(row.threshold) + "<br>"
    entries = entries + "amount in bag: " + str(row.amountinbag) + "<br>"
    entries = entries + "network: " + row.network + "<br>"
    for row2 in row.users:
      entries = entries + "user in bag: " + str(row2.firstname) + '<br>'
    for row2 in row.orders:
      entries = entries + "order: " + str(row2.price) + '<br>'
    entries = entries + "<br><br>"
  return entries

@app.route('/newbag', methods=['GET', 'POST'])
def newbag():
  if not session.get('logged_in'):
    abort(401)
  if request.method == 'POST':
    bag = Bag(request.form['store'], request.form['threshold'], 0, request.form['network'])
    db_session.add(bag)
    db_session.commit()
    return redirect(url_for('home'))
  return render_template('newbagform.html')

# shows all of the relevant information for a store's bag
@app.route('/bag/<bagid>', methods=['GET', 'POST'])
def bagpage(bagid):
  if not session.get('logged_in'):
    abort(401)
  bag = Bag.query.filter_by(id=bagid).first()
  if request.method == 'POST':
    # check the validity of input, if something is wrong, return the page with error messages where appropriate
    errorfound = False
    try:
      price = float(request.form['price'])
      if price < 0:
        flash("Invalid price", "priceerror")
        errorfound = True
    except ValueError:
      flash("Invalid price", "priceerror")
      errorfound = True

    # check if any fields were left empty
    if not request.form['itemurl']:
      flash("Please input the item's URL", "missingurlerror")
      errorfound = True
    if not request.form['price']:
      flash("Please input the price of the item", "missingpriceerror")
      errorfound = True
    if not request.form['details']:
      flash("Please enter details about your order", "missingdetailserror")
      errorfound = True
    if errorfound:
      return redirect(url_for('bagpage', bagid=bagid))

    bag.amountinbag = bag.amountinbag - price
    # add the user to the bag

    ship = False
    if 'ship' in request.form:
      ship = True
    curorder = Order.query.filter_by(id=session.get('userid')).first()
    db_session.delete(order)
    db_session.commit()
    # add the user's order to the bag
    order = Order(request.form['itemurl'], request.form['price'], request.form['details'], ship, None, None, None, None, None, bag.id, user.id)
    bag.orders.append(order)
    db_session.add(order)
    db_session.commit()
    flash("Your purchase of " + order.url + " has been added to the " + bag.store + " bag!", "addmessage")
    return redirect(url_for('bagpage', bagid=bagid))
  return render_template('bagpage.html', bag=bag, userid=session.get('userid'))


# displays all of the users' bags
@app.route('/mybags/<userid>')
def mybags(userid):
  if not session.get('logged_in'):
    abort(401)
  if not session.get('userid') == userid:
    return "Hey dickhead, you're not supposed to be here"
  user = User.query.filter_by(id = userid).first()  
  userbags = Bag.query.join(Bag.users, aliased=True).filter_by(id=userid)
  userorders = []
  bags = ""
  for bag in userbags:
    tuple = (Order.query.filter_by(bag_id=int(bag.id), user_id=userid).all(), str(bag.store))
    userorders.append(tuple)
  return render_template('mybags.html', mybags=userbags, userorders=userorders, userid=user.id, user=user)

# confirmation page for removing an order
@app.route('/removeorder/<orderid>')
def removeorder(orderid):
  if not session.get('logged_in'):
    abort(401)
  order = Order.query.filter_by(id=orderid).first()
  bag = Bag.query.filter_by(id=order.bag_id).first()
  return render_template('removeorder.html', order=order, bag=bag, userid=session.get('userid'))

# removed order, link back to original page
@app.route('/removed/<orderid>')
def removed(orderid):
  if not session.get('logged_in'):
    abort(401)
  order = Order.query.filter_by(id=orderid).first()
  bag = Bag.query.filter_by(id=order.bag_id).first()
  bag.amountinbag = bag.amountinbag - order.price

  # delete the order
  db_session.delete(order)  
  db_session.commit()

  # if the user has no more orders from that store, remove that store from the user's bags
  user = User.query.filter_by(id=session.get('userid')).first()
  orders = Order.query.filter_by(bag_id=bag.id, user_id=user.id).all()
  if not orders:
    user.bag.remove(bag)
    db_session.commit()

  return render_template('removed.html', userid=user.id, bag=bag)


#----------------------------------------
# facebook authentication
#----------------------------------------


FACEBOOK_APP_ID = '366391460148417'
FACEBOOK_APP_SECRET = '30806e2f0f0308ba2f0adc634455d231'

oauth = OAuth()

facebook = oauth.remote_app('facebook',
    base_url='https://graph.facebook.com/',
    request_token_url=None,
    access_token_url='/oauth/access_token',
    authorize_url='https://www.facebook.com/dialog/oauth',
    consumer_key=FACEBOOK_APP_ID,
    consumer_secret=FACEBOOK_APP_SECRET,
    request_token_params={'scope': ('email, ')}
)

@facebook.tokengetter
def get_facebook_token():
  return session.get('facebook_token')

def pop_login_session():
  session.pop('logged_in', None)
  session.pop('facebook_token', None)

@app.route("/facebook_login")
def facebook_login():
  return facebook.authorize(callback=url_for('facebook_authorized',next=request.args.get('next'), _external=True))

@app.route("/facebook_authorized")
@facebook.authorized_handler
def facebook_authorized(resp):
    next_url = request.args.get('next') or url_for('home')
    if resp is None or 'access_token' not in resp:
        return redirect(next_url)

    session['facebook_token'] = (resp['access_token'], '')
    fbuser = facebook.get('me').data
    if User.query.filter_by(email = fbuser['email']).first() == None:
      user = User(fbuser['first_name'], fbuser['last_name'], fbuser['email'], None, '')
      db_session.add(user)
      db_session.commit()
    
    user = User.query.filter_by(email = fbuser['email']).first()
    session['userid'] = user.id

    if user.isauthenticated:
      session['logged_in'] = True
      return redirect(url_for('home'))
    return redirect(url_for('cas'))

@app.route("/logout")
def logout():
    pop_login_session()
    return redirect(url_for('fblogin'))

