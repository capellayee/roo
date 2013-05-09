from __future__ import with_statement
from contextlib import closing
from Roo.database import db_session
from flask import Flask
from flask.ext.mail import Mail

#configuration
DATABASE = '/tmp/flasktest.db'
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'

app = Flask(__name__)
app.config.from_object(__name__)
app.config.from_envvar('FLASKR_SETTINGS', silent=True)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = 'themilkmanshipping@gmail.com'
app.config['MAIL_PASSWORD'] = 'brian333'
app.config['DEFAULT_MAIL_SENDER'] = 'themilkmanshippinggmail.com'


def max_function(a,b):
  return (max(a,b)

app.jinja_env.globals.update(max_function=max_function)

mail = Mail(app)


import Roo.views

@app.teardown_request
def teardown_request(exception):
  db_session.remove()

