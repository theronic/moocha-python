from flask import Blueprint, jsonify, request
from wtforms import Form, TextField, validators
from notify import gt, emailer

blueprint = Blueprint('api', __name__)

@blueprint.route('/status')
def status():
	return jsonify(
		success=True,
		message="Ok.",
	)

class SearchForm(Form):
	query = TextField('query', [validators.Length(min=1, max=256)])
	category = TextField('category') 

@blueprint.route('/search', methods=['GET'])
def search():
	form = SearchForm(request.args)
	if form.validate():
		search_results = gt.search(form.query.data, form.category.data)	
		return jsonify(
			success=True,
			message="Recieved form.",
			results=search_results,
		)

@blueprint.route('/get_categories', methods=['GET'])
def get_categories():
	return jsonify(
		success=True,
		message="Successfully retrieved categories.",
		categories=gt.categories,
		)

class SendEmailForm(Form):
	query = TextField('query', [validators.Length(min=1, max=256)])
	category = TextField('category') 
	email_address = TextField('email_address')

@blueprint.route('/send_search_results', methods=['GET'])
def send_search_results():
	form = SendEmailForm(request.args)
	if form.validate():
		search_results = gt.search(form.query.data, form.category.data)
		emailer.send_email(form.email_address.data, 'results', 'results.html', {
			'results': search_results,
			})
		return jsonify(
			success=True,
			message="Successfully sent email."
			)
