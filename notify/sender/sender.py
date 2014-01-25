from notify.models import EmailRule, Advertisement
from sqlalchemy import or_, and_
import datetime
import logging
from notify import config
from notify.emailer import Emailer
logger = logging.getLogger(__name__)


class Sender(object):
	def __init__(self, db, searcher):
		self.db = db
		self.searcher = searcher
		self.emailer = Emailer(config)

	def get_email_rules(self, timedelta):
		"""Get the email rules that have not been sent in the last timedelta.
		"""
		now = datetime.datetime.now()
		email_rules = (self.db.session.query(EmailRule)
			.filter(or_(EmailRule.last_sent < now - timedelta, EmailRule.last_sent == None)))
		number_of_email_rules = email_rules.count()
		logger.debug('Got %d email rules.', number_of_email_rules)
		return email_rules, number_of_email_rules
		
	def send_emails(self):
		timedelta = datetime.timedelta(seconds=10)
		logger.info('Sending Emails.')
		logger.debug('Getting email rules.')
		email_rules, count = self.get_email_rules(timedelta)
		for email_rule in email_rules:
			self.process_email_rule(email_rule)
		logger.info('Finished sending emails.')

	def process_email_rule(self, email_rule):
		now = datetime.datetime.now()
		logger.debug('Dealing with email rule: %s', email_rule)
		search_results = self.searcher.search(email_rule.query, email_rule.category)
		# Get a list of new advertisements since the last email.
		new_results = list()
		for result in search_results:
			matching_ad = (self.db.session.query(Advertisement)
				.filter(and_(Advertisement.title == result.title, Advertisement.description == result.description))
				.first())
			if not matching_ad:
				new_results.append(result)
				self.db.session.add(result)
		# Send the email.
		self.emailer.send_email(
			address=email_rule.email_address,
			subject='New Deals',
			template_path='results.html',
			values={
				'results': new_results,
			},
		)
		# Set the last_sent date to now.
		email_rule.last_sent = now
		self.db.session.add(email_rule)
		self.db.session.commit()
		