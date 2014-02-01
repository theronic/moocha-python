from flask import Blueprint, jsonify, request
from wtforms import Form, TextField, validators
from moocha import searcher_instance 
from moocha .api import blueprint

"""While internally locations are assoctiated with the searcher,
they are exposed as their own entity in the api.
"""

@blueprint.route('/locations/', methods=['GET'])
def get_locations():
	return jsonify(
		success=True,
		message="Successfully retrieved locations.",
		result={
			'locations': searcher_instance.get_locations(),
		},
		meta={
			'count': len(searcher_instance.get_locations())
		}
	)

