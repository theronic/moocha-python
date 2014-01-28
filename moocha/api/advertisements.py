from flask import Blueprint, jsonify, request
from wtforms import Form, TextField, validators
from notify import searcher_instance, db
from notify.api import blueprint
from notify.models import Advertisement

@blueprint.route('/advertisements/', methods=['GET'])
def get_advertisements():
	advertisement_query = db.session.query(Advertisement)
	count = advertisement_query.count()
	advertisements = [ad.to_dict() for ad in advertisement_query.all()]
	return jsonify(
		success=True,
		result={
			'advertisements': advertisements,
		},
		meta={
			'count': count
		}
	)
