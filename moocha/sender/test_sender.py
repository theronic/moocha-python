import unittest
from sender import Sender
from moocha import create_app, db
from moocha.models import EmailRule, Advertisement
import datetime

class TestSender(unittest.TestCase):
	def setUp(self):
		app = create_app()
		db.create_all()

	def tearDown(self):
		db.session.remove()
		db.drop_all()

	def test_send_update_email_sets_email_rules_last_sent(self):
		"""Test that send_update_email sets email_rule's last sent.
		"""
		sender = Sender(
			db=db,
			searcher=None # Not touched by send_update_email.
		)
		mock_email_rule = EmailRule(
			email_address='mock_address@example.co.za',
			query='mock query',
			category='mock category',
		)
		# Assert that the email_rule's last_sent is None.
		self.assertIsNone(mock_email_rule.last_sent_on)
		mock_new_ads = [
			Advertisement(title='foo', description='bar', source='foobar')
		]
		def mock_send_email(*args, **kwargs):
			pass 
		sender.emailer.send_email = mock_send_email
		sender.send_update_email(
			email_rule=mock_email_rule,
			new_ads=mock_new_ads,
		)
		# Assert that the email_rule's last_sent is not None.
		self.assertIsNotNone(mock_email_rule.last_sent_on)

	def test_send_update_email_calls_send_email_correctly(self):
		"""Test that send_update_email calls send_email with correct arguments.
		"""
		sender = Sender(
			db=db,
			searcher=None # Not touched by send_update_email.
		)
		mock_address = 'mock_address@example.co.za'
		mock_email_rule = EmailRule(
			email_address=mock_address,
			query='mock query',
			category='mock category',
		)
		# Assert that the email_rule's last_sent is None.
		self.assertIsNone(mock_email_rule.last_sent_on)
		mock_new_ads = [
			Advertisement(title='foo', description='bar', source='foobar')
		]
		#TODO: Asserts with source address.
		def mock_send_email(address, subject_template_path, body_template_path, source_address, template_args):
			self.assertEqual(address, mock_address)
			self.assertEqual(subject_template_path, 'new_matching_ads_update/subject.html')
			self.assertEqual(body_template_path, 'new_matching_ads_update/body.html')
			self.assertIsInstance(template_args, dict)
			self.assertIn('new_ads', template_args)
			self.assertIsInstance(template_args['new_ads'], list)
			self.assertEqual(template_args['new_ads'], mock_new_ads)
		sender.emailer.send_email = mock_send_email
		sender.send_update_email(
			email_rule=mock_email_rule,
			new_ads=mock_new_ads,
		)


	def test_list_new_ads_when_no_ads_match_email_rule(self):
		"""Test that list_new_ads returns an empty lits when there are no ads in the db.
		"""
		sender = Sender(
			db=db,
			searcher=None, # Not touched by upsert_ads
		)
		mock_email_rule = EmailRule('foo', 'bar', 'wap')
		expected_result = list()
		class MockSearcher(object):
			def search(*args, **kwargs):
				return []
		sender.searcher = MockSearcher()
		results = [res for res in sender.list_new_ads(mock_email_rule)]
		self.assertEqual(results, expected_result)

	def test_list_new_ads_when_no_have_been_seen_yet(self):
		"""Test that list_new_ads returns all the ads when no ads have been
		seen by the email_rule yet.
		"""
		sender = Sender(
			db=db,
			searcher=None, # Not touched by upsert_ads
		)
		mock_email_rule = EmailRule('foo', 'bar', 'wap')
		mock_ads = [
			Advertisement('foo', 'bar', 'wop'),
			Advertisement('foo', 'bar', 'wop'),
			Advertisement('foo', 'bar', 'wop'),
			Advertisement('foo', 'bar', 'wop'),
		]
		class MockSearcher(object):
			def search(*args, **kwargs):
				return mock_ads
		sender.searcher = MockSearcher()
		results = [res for res in sender.list_new_ads(mock_email_rule)]
		expected_result = mock_ads
		self.assertEqual(results, expected_result)

	def test_list_new_ads_ignores_seen_ads(self):
		"""Test that list_new_ads does not return ads that have been seen
		by the email_rule.
		"""
		sender = Sender(
			db=db,
			searcher=None, # Not touched by upsert_ads
		)
		mock_email_rule = EmailRule('foo', 'bar', 'wap')
		mock_ads = [
			Advertisement('foo1', 'bar', 'wop'),
			Advertisement('foo2', 'bar', 'wop'),
			Advertisement('foo3', 'bar', 'wop'),
			Advertisement('foo4', 'bar', 'wop'),
		]
		mock_email_rule.advertisements.append(mock_ads[0])
		class MockSearcher(object):
			def search(*args, **kwargs):
				return mock_ads
		sender.searcher = MockSearcher()
		results = [res for res in sender.list_new_ads(mock_email_rule)]
		expected_result = mock_ads[1:]
		self.assertEqual(results, expected_result)

	def test_get_unprocessed_email_rules_ignores_recent_rules(self):
		"""Test that get_unprocessed_email_rules does not retrieve email_rules that
		have been recently updated.
		"""
		now = datetime.datetime.now()
		sender = Sender(
			db=db,
			searcher=None, # Not touched.
		)
		mock_email_rule = EmailRule('foo', 'bar', 'wap')
		mock_email_rule.last_sent_on = now
		db.session.add(mock_email_rule)
		db.session.commit()
		timedelta = datetime.timedelta(days=1)
		result = [x for x in sender.get_unprocessed_email_rules(timedelta)]
		expected_result = list()
		self.assertEqual(result, expected_result)

	def test_get_unprocessed_email_rules_returns_untouched_new_rules(self):
		"""Test that get_unprocessed_email_rules returns rules that have never
		been updated.
		"""
		now = datetime.datetime.now()
		sender = Sender(
			db=db,
			searcher=None, # Not touched.
		)
		mock_email_rule = EmailRule('foo', 'bar', 'wap')
		db.session.add(mock_email_rule)
		db.session.commit()
		timedelta = datetime.timedelta(seconds=1)
		result = [x for x in sender.get_unprocessed_email_rules(timedelta)]
		expected_result = [mock_email_rule]
		self.assertEqual(result, expected_result)

	def test_get_unprocessed_email_rules_returns_old_rules(self):
		"""Test that get_unprocessed_email_rules returns rules that have been
		updated longer that the specified timedelta ago.
		"""
		now = datetime.datetime.now()
		sender = Sender(
			db=db,
			searcher=None, # Not touched.
		)
		mock_email_rule = EmailRule('foo', 'bar', 'wap')
		mock_email_rule.last_sent_on = now - datetime.timedelta(days=1)
		db.session.add(mock_email_rule)
		db.session.commit()
		timedelta = datetime.timedelta(seconds=1)
		result = [x for x in sender.get_unprocessed_email_rules(timedelta)]
		expected_result = [mock_email_rule]
		self.assertEqual(result, expected_result)

	def test_process_email_rule_calls_list_new_ads_correctly(self):
		class MockSearcher(object):
			def search(self, *args, **kwargs):
				return []
		class MockEmailer(object):
			def send_email(self, *args, **kwargs):
				pass
		sender = Sender(
			db=db,
			searcher=MockSearcher(),
		)
		sender.emailer = MockEmailer()
		mock_email_rule = EmailRule('foo', 'bar', 'wop')
		def mock_list_new_ads(email_rule):
			self.assertEqual(email_rule, mock_email_rule)
			return []
		sender.list_new_ads = mock_list_new_ads
		sender.process_email_rule(mock_email_rule)

	def test_process_email_rule_calls_deduplicate_ads_correctly(self):
		class MockSearcher(object):
			def search(self, *args, **kwargs):
				return []
		class MockEmailer(object):
			def send_email(self, *args, **kwargs):
				pass
		sender = Sender(
			db=db,
			searcher=MockSearcher(),
		)
		sender.emailer = MockEmailer()
		mock_email_rule = EmailRule('foo', 'bar', 'wop')
		mock_ads = [Advertisement('foo', 'bar', 'wop')]
		def mock_list_new_ads(*args, **kwargs):
			return mock_ads
		sender.list_new_ads = mock_list_new_ads
		def mock_deduplicate_ads(ads):
			self.assertEqual(ads, mock_ads)
			return ads
		sender.deduplicate_ads = mock_deduplicate_ads
		sender.process_email_rule(mock_email_rule)

	def test_process_email_rule_calls_update_email_rules_seen_ads_correctly(self):
		class MockSearcher(object):
			def search(self, *args, **kwargs):
				return []
		class MockEmailer(object):
			def send_email(self, *args, **kwargs):
				pass
		sender = Sender(
			db=db,
			searcher=MockSearcher(),
		)
		sender.emailer = MockEmailer()
		mock_email_rule = EmailRule('foo', 'bar', 'wop')
		mock_ads = [Advertisement('foo', 'bar', 'wop')]
		def mock_list_new_ads(*args, **kwargs):
			return mock_ads
		sender.list_new_ads = mock_list_new_ads
		def mock_deduplicate_ads(ads):
			self.assertEqual(ads, mock_ads)
			return ads
		sender.deduplicate_ads = mock_deduplicate_ads
		def mock_update_email_rules_seen_ads(email_rule, ads):
			self.assertEqual(email_rule, mock_email_rule)
			self.assertEqual(ads, mock_ads)
		sender.update_email_rules_seen_ads = mock_update_email_rules_seen_ads
		sender.process_email_rule(mock_email_rule)
	


	def test_process_email_rule_calls_upsert_ads_correctly(self):
		class MockSearcher(object):
			def search(self, *args, **kwargs):
				return []
		class MockEmailer(object):
			def send_email(self, *args, **kwargs):
				pass
		sender = Sender(
			db=db,
			searcher=MockSearcher(),
		)
		sender.emailer = MockEmailer()
		mock_email_rule = EmailRule('foo', 'bar', 'wop')
		mock_ads = [Advertisement('foo', 'bar', 'wop')]
		def mock_list_new_ads(*args, **kwargs):
			return mock_ads
		sender.list_new_ads = mock_list_new_ads
		def mock_upsert_ads(*args, **kwargs):
			pass
		sender.upsert_ads = mock_upsert_ads
		def mock_send_update_email(email_rule, new_ads):
			self.assertEqual(email_rule, mock_email_rule)
			self.assertEqual(new_ads, mock_new_ads)
		sender.process_email_rule(mock_email_rule)

	def test_process_email_rules_calls_guer_correctly(self):
		"""Test that process_email_rules calls get_unprocessed_email_rules
		correctly.
		"""
		sender = Sender(
			db=db,
			searcher=None,
		)
		def mock_get_unprocessed_email_rules(timedelta):
			self.assertIsInstance(timedelta, datetime.timedelta)
			return []
		sender.get_unprocessed_email_rules = mock_get_unprocessed_email_rules 
		sender.process_email_rules()

	def test_process_email_rules_calls_process_email_rule_correctly(self):
		sender = Sender(
			db=db,
			searcher=None,
		)
		mock_email_rule = EmailRule('foo', 'bar', 'bas')
		def mock_get_unprocessed_email_rules(timedelta):
			self.assertIsInstance(timedelta, datetime.timedelta)
			return [mock_email_rule]
		sender.get_unprocessed_email_rules = mock_get_unprocessed_email_rules 
		def process_email_rule(email_rule):
			self.assertEqual(email_rule, mock_email_rule)
		sender.process_email_rule = process_email_rule
		sender.process_email_rules()
