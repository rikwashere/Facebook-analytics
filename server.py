from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash, jsonify
from wtforms.validators import DataRequired
from wtforms import StringField
from flask_wtf import Form
import sqlite3
import os

app = Flask(__name__)

class SearchForm(Form):
    search = StringField('search', validators=[DataRequired()])

app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'facebook.db'),
    DEBUG=True,
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='default'

))
app.config.from_envvar('FLASKR_SETTINGS', silent=True)

def connect_db():
    """Connects to the specific database."""
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv

def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()

    g.sqlite_db.row_factory = sqlite3.Row
    return g.sqlite_db

def query_db(query, args=(), one=False):
	cur = get_db().execute(query, args)
	rv = cur.fetchall()
	cur.close()
	return (rv[0] if rv else None) if one else rv    

@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()

@app.route('/', methods=['POST', 'GET'])
def index():
	db = get_db()
	posts = query_db('SELECT * FROM facebook ORDER BY time_stamp DESC')
	search_form = SearchForm()	
	num_post = 20
	# rebuild
	return render_template('show_posts.html', posts=posts[:num_post], form=search_form)
    
@app.route('/search/', methods=['POST'])
def handle_data():
	url = (request.form['search'], )
	db = get_db()
	app.logger.info('Looking for URL: %s', request.form['search'])

	post = query_db('SELECT * FROM facebook WHERE link = ?', url)
	app.logger.info('Results: %s' % post)
	search_form = SearchForm()	
	return render_template('show_posts.html', posts=post, form=search_form)

