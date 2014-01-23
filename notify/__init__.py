from flask import Flask
from gumtree import Gumtree
from emailer import Emailer

app = Flask(__name__)

app.config.from_pyfile('config.py')

gt = Gumtree(app)

emailer = Emailer(app)