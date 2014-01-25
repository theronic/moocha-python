import unittest
from sender import Sender
from notify import create_app, db
from notify.models import EmailRule
import datetime

class TestSender(unittest.TestCase):
	def setUp(self):
		app = create_app()
		db.create_all()

	def tearDown(self):
		db.session.remove()
		db.drop_all()

	def test_process_email_rule_with_no_new_advertisements(self):
		class Searcher(object):
			pass
		sender = Sender(db, Searcher())
		def search(query, category):
			return []
		def send_email(*args, **kwargs):
			return True
		sender.searcher.search = search
		sender.emailer.send_email = send_email
		email_rule = EmailRule('avoid3d@gmail.com', 'foo', 'bar')
		sender.process_email_rule(email_rule)

	def test_get_email_rules_with_no_rules(self):
		"""Sender correctly fetches no rules when there arn't any.
		"""
		sender = Sender(db, None)
		timedelta = datetime.timedelta(1)
		rules, count = sender.get_email_rules(timedelta)
		self.assertEqual(count, 0)
		for rule in rules:
			self.fail('Iterating over supposedly empty rules ran at least once.')

	def test_get_email_rules_with_rules(self):
		"""Sender correctly fetches email rues.
		"""
		sender = Sender(db, None)
		# Insert an email rule.
		email_rule = EmailRule('avoid3d@gmail.com', 'foo', 'bar')
		db.session.add(email_rule)
		db.session.commit()
		timedelta = datetime.timedelta(1)
		rules, count = sender.get_email_rules(timedelta)
		self.assertEqual(count, 1)
		email_rules = [rule for rule in rules]
		self.assertEqual(email_rule, email_rules[0])
