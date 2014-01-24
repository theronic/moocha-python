import unittest
from notify import app, gt
import json

class TestAPI(unittest.TestCase):
	def setUp(self):
		self.app = app.test_client()

	def test_status(self):
		result = json.loads(self.app.get('/api/status').data)
		# The success flag is present and True.
		self.assertIn('success', result)
		self.assertIsInstance(result['success'], bool)
		self.assertTrue(result['success'])
		# The message is present and is a string.
		self.assertIn('message', result)
		self.assertIsInstance(result['message'], basestring)

	def test_search(self):
		result = json.loads(self.app.get('/api/search?query=hello').data)
		pass

	def test_get_categories(self):
		result = json.loads(self.app.get('/api/get_categories').data)
		# The success flag is present and True.
		self.assertIn('success', result)
		self.assertIsInstance(result['success'], bool)
		self.assertTrue(result['success'])
		# The message is present and is a string.
		self.assertIn('message', result)
		self.assertIsInstance(result['message'], basestring)
		# The categories are present and correct.
		self.assertIn('categories', result)
		self.assertIsInstance(result['categories'], dict)
		self.assertEqual(result['categories'], gt.categories)