from flask.ext.testing import TestCase
from moocha import create_app, searcher_instance
import json

class TestCategories(TestCase):
	def create_app(self):
		app = create_app()
		app.config['TESTING'] = True
		return app

	def get_list(self, result, resource_name):
		self.assertIn('success', result)
		self.assertTrue(result['success'])
		self.assertIn('meta', result)
		self.assertIn('count', result['meta'])
		count = result['meta']['count']
		self.assertIn('result', result)
		self.assertIn(resource_name, result['result'])
		return result['result'][resource_name], count

	def test_get_categories(self):
		response = self.client.get('/api/categories/')
		self.assertEqual(response.status_code, 200)
		result = response.json
		categories, count = self.get_list(result, 'categories')

		self.assertEqual(categories, searcher_instance.get_categories())