from __future__ import with_statement
from contextlib import closing
from Roo.database import db_session
from flask import Flask
from flask.ext.mail import Mail

#configuration
#DATABASE = '/tmp/flasktest.db'
DEBUG = True
SECRET_KEY = 'development key'
#USERNAME = 'admin'
#PASSWORD = 'default'

app = Flask(__name__)
app.config.from_object(__name__)
#app.config.from_envvar('FLASKR_SETTINGS', silent=True)

mail = Mail(app)

import Roo.views

@app.teardown_request
def teardown_request(exception):
  db_session.remove()

