from flask import Blueprint, jsonify, request
from wtforms import Form, TextField, validators
from notify import searcher_instance 
from notify.api import blueprint

class SearchForm(Form):
	query = TextField('query', [validators.Length(min=1, max=256)])
	category = TextField('category') 

@blueprint.route('/search', methods=['GET'])
def search():
	form = SearchForm(request.args)
	if not form.validate():
		return jsonify(
			success=False,
			message=form.errors,
			), 400

	search_results = searcher_instance.search(form.query.data, form.category.data)	
	return jsonify(
		success=True,
		message="Searched.",
		results=[search_result.to_dict() for search_result in search_results],
	)

@blueprint.route('/search/categories/', methods=['GET'])
def get_categories():
	return jsonify(
		success=True,
		message="Successfully retrieved categories.",
		categories=searcher_instance.get_categories(),
		)

