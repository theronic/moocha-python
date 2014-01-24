import unittest
from sender import Sender
from notify import create_app, db
from notify.models import EmailRule

class TestSender(unittest.TestCase):
	def setUp(self):
		app = create_app()
		db.create_all()

	def tearDown(self):
		db.session.remove()
		db.drop_all()

	def test_process_email_rule(self):
		sender = Sender(db)
		email_rule = EmailRule('avoid3d@gmail.com')
		sender.process_email_rule(email_rule)

	def test_get_email_rules_with_no_rules(self):
		"""Sender correctly fetches no rules when there arn't any.
		"""
		sender = Sender(db)
		rules, count = sender.get_email_rules()
		self.assertEqual(count, 0)
		for rule in rules:
			self.fail('Iterating over supposedly empty rules ran at least once.')

	def test_get_email_rules_with_rules(self):
		"""Sender correctly fetches email rues.
		"""
		sender = Sender(db)
		# Insert an email rule.
		email_rule = EmailRule('avoid3d@gmail.com')
		db.session.add(email_rule)
		db.session.commit()
		rules, count = sender.get_email_rules()
		self.assertEqual(count, 1)
		email_rules = [rule for rule in rules]
		self.assertEqual(email_rule, email_rules[0])
