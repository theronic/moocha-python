from mock import Mock
import unittest
from flask.ext.testing import TestCase
from moocha import create_app, db
from moocha.gumtree import Gumtree
from moocha.api import email_rules
from moocha.models import Advertisement
import json

class TestEmailRules(TestCase):
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

	def test_get_advertisements_works_with_no_ads(self):
		response = self.client.get('/api/advertisements/')
		self.assertEqual(response.status_code, 200)
		result = response.json
		ads, count = self.get_list(result, 'advertisements')
		self.assertEqual(count, 0)
		self.assertEqual(len(ads), 0)
		self.assertEqual(ads, list())

	def test_get_advertisement_works_with_ads(self):
		ad = Advertisement('', '', '')
		db.session.add(ad)
		db.session.commit()
		response = self.client.get('/api/advertisements/')
		self.assertEqual(response.status_code, 200)
		result = response.json
		ads, count = self.get_list(result, 'advertisements')
		self.assertEqual(count, 1)
		self.assertEqual(len(ads), 1)
		self.assertEqual(ads[0], ad.to_dict())
