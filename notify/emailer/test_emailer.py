import unittest
from emailer import Emailer
from notify import config
from jinja2 import Template


class MockApp(object):
	def __init__(self, config):
		self.config = {
			'AWS_ACCESS_KEY_ID': config.AWS_ACCESS_KEY_ID,
			'AWS_SECRET_KEY': config.AWS_SECRET_KEY,
			'EMAILER_SOURCE_ADDRESS': config.EMAILER_SOURCE_ADDRESS,
		}	


class TestEmailer(unittest.TestCase):
	def setUp(self):
		mock_app = MockApp(config)
		self.emailer = Emailer(mock_app)

	def test_send_email(self):
		self.emailer.send_email(
			address='avoid3d@gmail.com',
			subject='hello',
			template=Template('Hello {{name}}!'),
			values={'name': 'Pierre Hugo'}
			)