import unittest
from notify import create_app, searcher_instance
import json

class TestAPI(unittest.TestCase):
	def setUp(self):
		app = create_app()
		self.app = app.test_client()

	def test_get_categories(self):
		result = json.loads(self.app.get('/api/search/categories/').data)
		# The success flag is present and True.
		self.assertIn('success', result)
		self.assertIsInstance(result['success'], bool)
		self.assertTrue(result['success'])
		# The message is present and is a string.
		self.assertIn('message', result)
		self.assertIsInstance(result['message'], basestring)
		# The categories are present and correct.
		self.assertIn('categories', result)
		self.assertIsInstance(result['categories'], list)
		self.assertEqual(result['categories'], searcher_instance.get_categories())