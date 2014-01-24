from flask import Blueprint, jsonify, request
from wtforms import Form, TextField, validators
from notify import emailer_instance

blueprint = Blueprint('api', __name__)

@blueprint.route('/status')
def status():
	return jsonify(
		success=True,
		message="Ok.",
	)

import search

