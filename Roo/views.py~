from Roo import app
from Roo.database import db_session
from Roo.models import User, Bag
from flask import Flask, request, session, g, redirect, url_for, \
	abort, render_template, flash

@app.route('/')
def show_users():
  users = User.query.all()
  return render_template('show_users.html', users=users)

@app.route('/all')
def home():
    entries = ""
    for row in User.query.all():
      entries = entries + "first name: " + row.firstname + '<br>'
      entries = entries + "last name: " + row.lastname + '<br>'
      entries = entries + "address: " + row.address + '<br>'
      if row.bag != None:
        entries = entries + "bags involved: " + str(row.bag.store) + '<br>'
      entries = entries + "email: " + row.email + '<br><br>'
      
    entries = entries + "<br><br><br><br><br>Now, the Bags:<br>"
    
    for row in Bag.query.all():
      entries = entries + "store name: " + row.store + "<br>"
      entries = entries + "threshold: " + str(row.threshold) + "<br>"
      entries = entries + "amount in bag: " + str(row.amountinbag) + "<br>"
      entries = entries + "network: " + row.network + "<br>"
      entries = entries + "users in bag: " + str(row.users[0].firstname) + '<br><br>'

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
