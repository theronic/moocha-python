from flask import Blueprint, jsonify, request
from wtforms import Form, TextField, validators
from moocha import searcher_instance 
from moocha .api import blueprint

"""While internally categories are assoctiated with the searcher,
they are exposed as their own entity in the api.
"""

@blueprint.route('/categories/', methods=['GET'])
def get_categories():
	return jsonify(
		success=True,
		message="Successfully retrieved categories.",
		result={
			'categories': searcher_instance.get_categories(),
		},
		meta={
			'count': len(searcher_instance.get_categories())
		}
	)

