from notify.models import EmailRule
import logging
logger = logging.getLogger(__name__)


class Sender(object):
	def __init__(self, db):
		self.db = db

	def get_email_rules(self):
		# For each email rule.
		email_rules = self.db.session.query(EmailRule)
		number_of_email_rules = email_rules.count()
		logger.debug('Got %d email rules.', number_of_email_rules)
		return email_rules, number_of_email_rules

		
	def send_emails(self):
		logger.info('Sending Emails.')
		logger.debug('Getting email rules.')
		email_rules, count = self.get_email_rules()
		for email_rule in email_rules:
			self.process_email_rule(email_rule)
		logger.info('Finished sending emails.')

	def process_email_rule(self, email_rule):
		logger.debug('Dealing with email rule: %s', email_rule)
		#TODO: Establish which offers are new.

