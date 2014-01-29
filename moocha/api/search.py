from flask import Blueprint, jsonify, request
from wtforms import Form, TextField, validators
from moocha import searcher_instance 
from moocha.api import blueprint

class SearchForm(Form):
	query = TextField('query', [validators.Length(min=1, max=256)])
	category = TextField('category', [validators.AnyOf(searcher_instance.get_categories())]) 

@blueprint.route('/search', methods=['GET'])
def search():
	form = SearchForm(request.args)
	if not form.validate():
		return jsonify(
			success=False,
			message=form.errors,
			), 400

	search_results = searcher_instance.search(
		query=form.query.data,
		category=form.category.data,
	)	
	return jsonify(
		success=True,
		message="Searchedlol.",
		result={
			'advertisements': [search_result.to_dict() for search_result in search_results],
		},
		meta={
			'count': len(search_results)
		}
	)
