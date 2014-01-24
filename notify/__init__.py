from flask import Flask, redirect
from flask.ext.sqlalchemy import SQLAlchemy
import logging
import config
from emailer import Emailer
from searcher import Searcher
logger = logging.getLogger('')
logger.setLevel(logging.DEBUG)
console_handler = logging.StreamHandler()
#formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
#console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

db = SQLAlchemy()

def create_app(db_uri='sqlite://'):
	app = Flask(__name__, static_folder='ui', static_url_path='')
	app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
	db.init_app(app)
	# Register redirect homepage.
	@app.route('/')
	def redirect_homepage():
		return redirect('/index.html')
	# Register api routes.
	import api
	app.register_blueprint(api.blueprint, url_prefix='/api')
	return app

emailer_instance = Emailer(config)

searcher_instance = Searcher()