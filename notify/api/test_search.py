from flask.ext.testing import TestCase
from notify import create_app, searcher_instance
import json

class TestAPI(TestCase):
	def create_app(self):
		app = create_app()
		app.config['TESTING'] = True
		return app

	def test_get_categories(self):
		result = self.client.get('/api/search/categories/').json
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