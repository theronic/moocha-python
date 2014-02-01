from flask import Blueprint, jsonify, request
from wtforms import Form, TextField, validators

blueprint = Blueprint('api', __name__)

@blueprint.route('/status')
def status():
	return jsonify(
		success=True,
		message="Ok.",
	)

import search
import advertisements
import email_rules
import sent_emails
import categories
import locations