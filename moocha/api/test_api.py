import unittest
from flask.ext.testing import TestCase
from notify import create_app 
from notify.gumtree import Gumtree
import json

gumtree_instance = Gumtree()

class TestStatus(TestCase):
	def create_app(self):
		app = create_app()
		return app

	def test_status(self):
		"""The route /api/status returns ok.
		"""
		result = self.client.get('/api/status').json
		# The success flag is present and True.
		self.assertIn('success', result)
		self.assertIsInstance(result['success'], bool)
		self.assertTrue(result['success'])
		# The message is present and is a string.
		self.assertIn('message', result)
		self.assertIsInstance(result['message'], basestring)
