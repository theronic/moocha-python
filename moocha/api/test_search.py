from mock import Mock
import unittest
from flask.ext.testing import TestCase
from moocha import create_app, db
from moocha.gumtree import Gumtree
from moocha.api import email_rules
from moocha.models import Advertisement
from moocha.api import search
import json

class TestSearch(TestCase):
	def setUp(self):
		db.create_all()

	def tearDown(self):
		db.session.remove()
		db.drop_all()

	def get_list(self, result, resource_name):
		self.assertIn('success', result)
		self.assertTrue(result['success'])
		self.assertIn('meta', result)
		self.assertIn('count', result['meta'])
		count = result['meta']['count']
		self.assertIn('result', result)
		self.assertIn(resource_name, result['result'])
		return result['result'][resource_name], count

	def create_app(self):
		app = create_app()
		return app

	def test_search_validates_query(self):
		search.searcher_instance.search = Mock(return_value=list())
		response = self.client.get('/api/search?query=hello&category=All%20Categories.Property.Short%20Term')
		self.assertEqual(response.status_code, 200)
		def check_search_returns_validation_error(query, should_fail=False):
			response = self.client.get('/api/search?query=%s&category=Computers' % query)
			self.assertEqual(response.status_code, 400)
			result = response.json
			self.assertFalse(result['success'])
		for query in ['', '*' * (256 + 1)]:
			check_search_returns_validation_error(query)

	def test_search_validates_category(self):
		search.searcher_instance.search = Mock(return_value=list())
		response = self.client.get('/api/search?query=hello&category=All%20Categories.Property.Short%20Term')
		self.assertEqual(response.status_code, 200)
		def check_search_returns_validation_error(query, should_fail=False):
			response = self.client.get('/api/search?query=foo&category=%s' % query)
			self.assertEqual(response.status_code, 400)
			result = response.json
			self.assertFalse(result['success'])
		for query in ['', 'hello']:
			check_search_returns_validation_error(query)

	def test_search_calls_searcher(self):
		search.searcher_instance.search = Mock(return_value=list())
		query = 'foo'
		self.client.get('/api/search?query=%s&category=%s' % (query, 'All%20Categories.Property.Short%20Term'))
		search.searcher_instance.search.assert_called_with(
			query=query,
			category = 'All Categories.Property.Short Term'
		)

	def test_search_returns_searchers_results(self):
		ad = Advertisement('foo', 'bar', 'baz')
		search.searcher_instance.search = Mock(return_value=[ad])
		response = self.client.get('/api/search?query=foo&category=All%20Categories.Property.Short%20Term')
		result = response.json
		ads, count = self.get_list(result, 'advertisements')
		self.assertEqual(count, 1)
		self.assertEqual(ads[0], ad.to_dict())
