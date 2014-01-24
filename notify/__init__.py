from flask import Flask, redirect
from gumtree import Gumtree
from emailer import Emailer

app = Flask(__name__, static_url_path='', static_folder='ui')

app.config.from_pyfile('config.py')

gt = Gumtree(app)

emailer = Emailer(app)

import api
app.register_blueprint(api.blueprint, url_prefix='/api')

# Redirect naked request to index.html
@app.route('/')
def redirect_to_index():
	return redirect('/index.html')
