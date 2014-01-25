from flask import jsonify
from notify import db
from notify.api import blueprint
from notify.models import SentEmail


@blueprint.route('/sent_emails/')
def get_sent_emails():
	sent_email_query = db.session.query(SentEmail)
	count = sent_email_query.count()
	sent_emails = sent_email_query.all()
	return jsonify(
		meta={
			'count': count,
		},
		results={
			'sent_emails': sent_emails,
		}
	)