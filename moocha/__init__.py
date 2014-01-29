from flask import Flask, redirect
from flask.ext.sqlalchemy import SQLAlchemy
import logging
logger = logging.getLogger('')
logger.setLevel(logging.DEBUG)
console_handler = logging.StreamHandler()
#formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
#console_handler.setFormatter(formatter)
logger.addHandler(console_handler)
from config import config

db = SQLAlchemy()

def create_app(*args, **kwagrs):
	app = Flask(__name__, static_folder='ui', static_url_path='')
	for key, value in config.values.items():
		app.config[key] = value
	db.init_app(app)
	# Register redirect homepage.
	@app.route('/')
	def redirect_homepage():
		return redirect('/index.html')
	# Register api routes.
	import api
	app.register_blueprint(api.blueprint, url_prefix='/api')
	return app

from searcher import Searcher
searcher_instance = Searcher()

from sender import Sender
sender_instance = Sender(db, searcher_instance)

app = create_app()