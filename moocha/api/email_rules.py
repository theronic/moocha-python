from flask import Blueprint, jsonify, request
from wtforms import Form, TextField, validators
from moocha import searcher_instance, db
from moocha.api import blueprint
from moocha.models import EmailRule

@blueprint.route('/email_rules/', methods=['GET'])
def get_email_rules():
	email_rule_query = db.session.query(EmailRule)
	count = email_rule_query.count()
	email_rules = [email_rule.to_dict() for email_rule in email_rule_query.all()]
	return jsonify(
		success=True,
		result={
			'email_rules': email_rules
		},
		meta={
			'count': count
		}
	)

class EmailRuleForm(Form):
	query = TextField('query', [validators.Length(min=1, max=256)])
	category = TextField('category', [validators.AnyOf(searcher_instance.get_categories())]) 
	email_address = TextField('email_address', [validators.Email()])

@blueprint.route('/email_rules/', methods=['POST'])
def create_email_rule():
	form = EmailRuleForm(**request.json)
	if not form.validate():
		return jsonify(
			success=False,
			message="Form did not pass validation.",
			errors=form.errors,
		), 400
	duplicate_email_rule = (db.session.query(EmailRule)
		.filter((EmailRule.email_address == form.email_address.data)
			& (EmailRule.query == form.query.data)
			& (EmailRule.category == form.category.data)
		).first())
	if duplicate_email_rule:
		return jsonify(
			success=False,
			message="Exactly the same email rule already exists.",
		), 409
	db.session.add(EmailRule(
		query=form.query.data,
		email_address=form.email_address.data,
		category=form.category.data,
	))
	db.session.commit()
	return jsonify(
		success=True,
		message="Successfully created new email rule.",
	)
