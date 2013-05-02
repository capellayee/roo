from Roo import app
from Roo.CASClient import CASClient
from Roo.database import db_session
from Roo.models import User, Bag, Order
from flask import Flask, request, session, g, redirect, url_for, \
	abort, render_template, flash
from flask_oauth import OAuth
from flask.ext.mail import Message
from Roo import mail

@app.route('/')
def fblogin():
  if not session.get('logged_in'):
    return render_template('login.html')
  else:
    return redirect(url_for('home'))

@app.route('/cas')
def cas():
  C = CASClient()
  netid = C.Authenticate()

  text = "Content-Type: text/html <br> Hello from the other side, " + str(netid) + '<br> print "Think of this as the main page of your application after ' + str(netid) + '  has been authenticated.'
  return text

@app.route('/email')
def email():
  text = ""
  for bag in Bag.query.all():
    text = text + bag.store
  msg = Message(text, sender="rooshipping@gmail.com", recipients=["pranav.gokhale.93@gmail.com"])
  mail.send(msg)
  return "Hi"


@app.route('/home')
def home():
  # store the bagid's for the featured stores on the carousel
  # brooks brothers
  brooksbrothersid = Bag.query.filter_by(store = 'Brooks Brothers').first().id
  # ralph lauren
  ralphlaurenid = Bag.query.filter_by(store = 'Ralph Lauren').first().id
  # j. crew
  jcrewid = Bag.query.filter_by(store = 'J. Crew').first().id

  userid = session.get('userid')
  allbags = Bag.query.all()
  user = User.query.filter_by(id=userid).first()
  mybags = []
  for b in user.bag:
    mybags.append(b)
  return render_template('carousel.html', userid=userid, brooksbrothersid=brooksbrothersid, ralphlaurenid=ralphlaurenid, jcrewid=jcrewid, mybags=mybags, allbags=allbags)

# a test page for the admin
@app.route('/all')
def all():
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
  if request.method == 'POST':
    bag = Bag(request.form['store'], request.form['threshold'], 0, request.form['network'])
    db_session.add(bag)
    db_session.commit()
    return redirect(url_for('home'))
  return render_template('newbagform.html')

# shows all of the relevant information for a store's bag
@app.route('/bag/<bagid>', methods=['GET', 'POST'])
def bagpage(bagid):
  #bag = Bag.query.filter_by(id=bagid).first()
  user = User.query.filter_by(id=session.get('userid')).first()
  return user.id
  #if request.method == 'POST':
  #  bag.amountinbag = bag.amountinbag + int(request.form['price'])
    # add the user to the bag
   # user = User.query.filter_by(id=session.get('userid')).first()
   # bag.users.append(user)
   # return user.id
    # add the user's order to the bag
   # order = Order(request.form['itemurl'], request.form['price'], request.form['quantity'], bag.id, user.id)
   # bag.orders.append(order)
   # db_session.add(order)
   # db_session.commit()
   # flash("Your purchase has been added")
   # return redirect(url_for('bagpage', bagid=bagid))
  #return render_template('bagpage.html', bag=bag)


# displays all of the users' bags
@app.route('/mybags/<userid>')
def mybags(userid):
  user = User.query.filter_by(id = userid).first()  
  userbags = Bag.query.join(Bag.users, aliased=True).filter_by(id=userid)
  userorders = []
  bags = ""
  for bag in userbags:
    tuple = (Order.query.filter_by(bag_id=int(bag.id), user_id=userid), str(bag.store))
    userorders.append(tuple)
  for order in userorders:
    bags = bags + order[0] + '<br>'
  return bags
  
#  return render_template('mybags.html', mybags=userbags, userorder=userorders)

# allows a user to add to a bag
@app.route('/addtobag/<userid>', methods=['GET', 'POST'])
def addtobag(userid):
    if request.method == 'POST':
        bag = Bag.query.filter_by(store = request.form['store']).first()
        bag.amountinbag = bag.amountinbag + int(request.form['price'])
        user = User.query.filter_by(id = userid).first()
        # add the user to the bag
        bag.users.append(user)
        # add the user's order to the bag
        order = Order(request.form['itemurl'], request.form['price'], request.form['quantity'], request.form['size'], bag.id, userid)
        bag.orders.append(order)
        db_session.add(order)
        db_session.commit()
        return redirect(url_for('mybags', userid=userid))
    return render_template('addtobagform.html')


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

    session['logged_in'] = True
    session['facebook_token'] = (resp['access_token'], '')

    fbuser = facebook.get('me').data
#    return fbuser['email']
    if User.query.filter_by(email = fbuser['email']).first() == None:
      user = User(fbuser['first_name'], fbuser['last_name'], fbuser['email'], '', '')
      db_session.add(user)
      db_session.commit()
    
    session['userid'] = User.query.filter_by(email = fbuser['email']).first().id
    return redirect(url_for('home'))

@app.route("/logout")
def logout():
    pop_login_session()
    return redirect(url_for('fblogin'))

