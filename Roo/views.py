from Roo import app
from Roo.database import db_session
from Roo.models import User
from flask import Flask, request, session, g, redirect, url_for, \
	abort, render_template, flash

@app.route('/')
def show_users():
  users = User.query.all()
  return render_template('show_users.html', users=users)

@app.route('/add', methods=['POST'])
def add_user():
  if not session.get('logged_in'):
	abort(401)
  user = User(request.form['firstname'], request.form['lastname'], request.form['email'], request.form['address'])
  db_session.add(user)
  db_session.commit()
  flash('New entry was succesfully posted')
  return redirect(url_for('show_users'))

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
	if request.form['username'] != app.config['USERNAME']:
		error = 'Invalid Username'
	elif request.form['password'] != app.config['PASSWORD']:
		error = 'Invalid password'
	else:
		session['logged_in'] = True
		flash('You were logged in')
		return redirect(url_for('show_users'))
  return render_template('login.html', error=error)

@app.route('/logout')
def logout():
  session.pop('logged_in', None)
  flash('You were logged out')
  return redirect(url_for('show_users'))
