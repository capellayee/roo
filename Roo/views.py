from Roo import app
from Roo.database import db_session
from Roo.models import User, Bag
from flask import Flask, request, session, g, redirect, url_for, \
	abort, render_template, flash
from flask_oauth import OAuth

@app.route('/')
def fblogin():
  if not session.get('logged_in'):
    return render_template('facebook_homepage.html')
  else:
    fbuser = facebook.get('me').data
    user = User(fbuser['first_name'], fbuser['last_name'], fbuser['email'], '', '')
    db_session.add(user)
    db_session.commit()

@app.route('/main')
def show_users():
  users = User.query.all()
  return render_template('show_users.html', users=users)

@app.route('/bootstraptest')
def bootstrap():
  return render_template('carousel.html')

@app.route('/all')
def home():
    entries = ""
    for row in User.query.all():
      entries = entries + "first name: " + row.firstname + '<br>'
      entries = entries + "last name: " + row.lastname + '<br>'
      entries = entries + "address: " + row.address + '<br>'
      for row2 in row.bag:
        entries = entries + "bags involved: " + str(row2.store) + '<br>'
      entries = entries + "email: " + row.email + '<br><br>'
      
    entries = entries + "<br><br><br><br><br>Now, the Bags:<br>"
    
    for row in Bag.query.all():
      entries = entries + "store name: " + row.store + "<br>"
      entries = entries + "threshold: " + str(row.threshold) + "<br>"
      entries = entries + "amount in bag: " + str(row.amountinbag) + "<br>"
      entries = entries + "network: " + row.network + "<br>"
      for row2 in row.users:
        entries = entries + "user in bag: " + str(row2.firstname) + '<br>'
      entries = entries + "<br><br>"
    return entries
      
@app.route('/add', methods=['POST'])
def add_user():
  if not session.get('logged_in'):
    abort(401)
  user = User(request.form['firstname'], request.form['lastname'], request.form['email'], request.form['password'], request.form['address'])
  db_session.add(user)
  db_session.commit()
  flash('New entry was succesfully posted')
  return redirect(url_for('show_users'))


@app.route('/newbag', methods=['GET', 'POST'])
def newbag():
    if request.method == 'POST':
        bag = Bag(request.form['store'], request.form['threshold'], request.form['amountinbag'], request.form['network'])
        db_session.add(bag)
        db_session.commit()
        return redirect(url_for('show_users'))
    return render_template('newbagform.html')


@app.route('/addtobag/<userid>', methods=['GET', 'POST'])
def addtobag(userid):
    if request.method == 'POST':
        bag = Bag.query.filter_by(store = request.form['store']).first()
        bag.amountinbag = bag.amountinbag + int(request.form['amountinbag'])
        user = User.query.filter_by(id = userid).first()
        bag.users.append(user)
        db_session.commit()
        return redirect(url_for('show_users'))
    return render_template('addtobagform.html')

@app.route('/remove/<userid>')
def remove_user(userid):
  if not session.get('logged_in'):
	abort(401)
  
  user = User.query.filter_by(id = userid).first()

  db_session.delete(user);
  db_session.commit();
  flash('User with Name:' + user.firstname + ' was removed')
  return redirect(url_for('show_users'))

@app.route('/login', methods=['GET', 'POST'])
def login():
  error = None
  if request.method == 'POST':
	if request.form['username'] == app.config['USERNAME']:
          session['logged_in'] = True
          flash('You were logged in')
          return redirect(url_for('show_users'))
        #if request.form['username'] != app.config['USERNAME']:
        user = request.form['username']
        queriedUser = User.query.filter_by(email = user).first()
        if user != queriedUser.email:
		error = 'Invalid Username'
#	elif request.form['password'] != app.config['PASSWORD']:
	elif request.form['password'] != queriedUser.password:
                error = 'Invalid password'
	else: # if its a non-admin user but successfully verified
		session['logged_in'] = True
		flash('You were logged in')
		return redirect(url_for('addtobag', userid=queriedUser.id))
  return render_template('login.html', error=error)

@app.route('/logout')
def logout():
  session.pop('logged_in', None)
  flash('You were logged out')
  return redirect(url_for('show_users'))

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
    return facebook.authorize(callback=url_for('facebook_authorized',
        next=request.args.get('next'), _external=True))

@app.route("/facebook_authorized")
@facebook.authorized_handler
def facebook_authorized(resp):
    next_url = request.args.get('next') or url_for('show_users')
    if resp is None or 'access_token' not in resp:
        return redirect(next_url)

    session['logged_in'] = True
    session['facebook_token'] = (resp['access_token'], '')

    return redirect(next_url)

@app.route("/logout")
def logout():
    pop_login_session()
    return redirect(url_for('show_users'))
