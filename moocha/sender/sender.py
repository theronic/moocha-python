from sqlalchemy import or_, and_
import datetime
import logging
from moocha import config
from moocha.emailer import Emailer
from moocha.models import EmailRule, Advertisement
logger = logging.getLogger(__name__)


class Sender(object):
	def __init__(self, db, searcher):
		self.db = db
		self.searcher = searcher
		self.emailer = Emailer(config)
		
	def process_email_rules(self):
		"""Send emails informing users of new ads which match there filters.
		Get all the email_rules that have not been processed in the last
		timedelta, check for new ads which match their filters and then
		send them an email showing these new ads.
		"""
		timedelta = datetime.timedelta(seconds=1)
		logger.debug('Getting email rules.')
		email_rules = self.get_unprocessed_email_rules(timedelta)
		for email_rule in email_rules:
			self.process_email_rule(email_rule)
		logger.info('Finished sending emails.')

	def process_email_rule(self, email_rule):
		"""Check for new ads which match the user's email_rule, and
		send them an email showing them these new ads. Also save
		the new ads to the database.
		"""
		logger.debug('Dealing with email rule: %s', email_rule)
		# Get the new search results for this email_rule.
		new_ads = self.list_new_ads(email_rule)
		# Upsert these new ads to the db.
		deduplicated_ads = self.deduplicate_ads(new_ads)
		# Add the deduplicated ads to the email rule.
		self.update_email_rules_seen_ads(email_rule, deduplicated_ads)
		# Send the email the email_rule pertains to.
		self.send_update_email(email_rule, new_ads)

	def update_email_rules_seen_ads(self, email_rule, ads):
		email_rule.advertisements += ads
		self.db.session.add(email_rule)
		self.db.session.commit()

	def get_unprocessed_email_rules(self, timedelta):
		"""Return the email_rules that have not been processed in the last <timedelta>.
		"""
		now = datetime.datetime.now()
		email_rules = (self.db.session.query(EmailRule)
			.filter(or_(EmailRule.last_sent_on < now - timedelta
				, EmailRule.last_sent_on == None)))
		logger.debug('Got %d email rules.', email_rules.count())
		return email_rules

	def list_new_ads(self, email_rule):
		"""Return a generator listing the ads which match the email_rule but which the user
		has not been notified of. (The results which match but have not been sent to
		the user.)
		"""
		logger.debug('Checking for new ads for email rule: %s' % email_rule)
		# Fetch ads matching the email rule.
		ads = self.searcher.search(
			query=email_rule.query,
			category=email_rule.category,
		)
		# Get the new results.
		for ad in ads:
			if ad not in email_rule.advertisements:
				yield ad 

	def deduplicate_ads(self, ads):
		"""Merge any matching ads between the ad argument and the db.
		"""
		logger.debug('Merging ads with db.')
		deduplicated_ads = list()
		for ad in ads:
			match = (self.db.session.query(Advertisement)
				.filter(Advertisement.title == ad.title)
				.first())
			if match:
				deduplicated_ads.append(match)
			else:
				self.db.session.add(ad)
				deduplicated_ads.append(ad)
		self.db.session.commit()
		return deduplicated_ads 

	def send_update_email(self, email_rule, new_ads):
		"""Send an email telling the user about new ads which match their query.
		"""
		logger.debug('Sending email to %s.', email_rule.email_address)
		now = datetime.datetime.now()
		self.emailer.send_email(
			address=email_rule.email_address,
			subject_template_path='new_matching_ads_update/subject.html',
			body_template_path='new_matching_ads_update/body.html',
			template_args={
			'new_ads': new_ads,
			'email_rule': email_rule,
			},
		)
		email_rule.last_sent_on = now
		self.db.session.add(email_rule)
		self.db.session.commit()
