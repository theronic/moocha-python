from flask import url_for
from mock import Mock
import unittest
from flask.ext.testing import TestCase
from moocha import create_app, db
from moocha.gumtree import Gumtree
from moocha.api import email_rules
from moocha.models import EmailRule
import json

class TestEmailRules(TestCase):
	def setUp(self):
		db.create_all()

	def tearDown(self):
		db.drop_all()
		db.session.remove()

	def json_post(self, url, data):
		return self.client.post(url,
			data=json.dumps(data),
			content_type='application/json',
			)

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

	def test_create_email_rule_uses_correct_wtform(self):
		"""Test that create_email_rule uses the EmailRuleForm wtform.
		"""
		mock = Mock(wraps=email_rules.EmailRuleForm)
		email_rules.EmailRuleForm = mock
		mock_data = {'hello': 'world'}
		self.json_post(url_for('api.create_email_rule'), mock_data)
		mock.assert_called_once_with(**mock_data)

	def test_create_email_rule_creates_email_rule_model_in_the_db(self):
		"""Test that create_email_rule correctly creates an EmailRule model
		in the db.
		"""
		mock_data = {
			'email_address': 'foo@bar.com',
			'query': 'search',
			'category': 'All Categories.Property.Short Term',
		}
		result = self.json_post(url_for('api.create_email_rule'), mock_data)
		self.assertEqual(db.session.query(EmailRule).count(), 1)
		email_rule = db.session.query(EmailRule).first()
		self.assertIsNotNone(email_rule)
		self.assertEqual(email_rule.email_address, mock_data['email_address'])
		self.assertEqual(email_rule.query, mock_data['query'])
		self.assertEqual(email_rule.category, mock_data['category'])

	def test_create_email_rule_does_not_create_duplicate_email_rules(self):
		mock_data = {
			'email_address': 'foo@bar.com',
			'query': 'search',
			'category': 'All Categories.Property.Short Term',
		}
		self.json_post(url_for('api.create_email_rule'), mock_data)
		self.assertEqual(db.session.query(EmailRule).count(), 1)
		self.json_post(url_for('api.create_email_rule'), mock_data)
		self.assertEqual(db.session.query(EmailRule).count(), 1)

	def test_create_email_rule_responds_correctly_to_duplicate_post(self):
		mock_data = {
			'email_address': 'foo@bar.com',
			'query': 'search',
			'category': 'All Categories.Property.Short Term',
		}
		self.json_post(url_for('api.create_email_rule'), mock_data)
		second_response = self.json_post(url_for('api.create_email_rule'), mock_data)
		self.assertEqual(second_response.status_code, 409)
		second_result = second_response.json
		self.assertFalse(second_result['success'])

	def test_create_email_rule_correctly_validates_email_address(self):
		def check_fails_validation(email_address):
			mock_data = {
				'email_address': email_address,
				'query': 'search',
				'category': 'All Categories.Property.Short Term',
			}
			response = self.json_post(url_for('api.create_email_rule'), mock_data)
			self.assertEqual(response.status_code, 400)
			result = response.json
			self.assertFalse(result['success'])
		for email_address in ['avoid3d', '']:
			check_fails_validation(email_address)

	def test_create_email_rule_correctly_validates_category(self):
		def check_fails_validation(category):
			mock_data = {
				'email_address': 'avoid3d@gmail.com',
				'query': 'search',
				'category': category,
			}
			response = self.json_post(url_for('api.create_email_rule'), mock_data)
			self.assertEqual(response.status_code, 400)
			result = response.json
			self.assertFalse(result['success'])
		for category in ['avoid3d', '']:
			check_fails_validation(category)

	def test_get_email_rules_handles_no_email_rules_in_db(self):
		response = self.client.get(url_for('api.get_email_rules'))
		self.assertEqual(response.status_code, 200)
		email_rules, count = self.get_list(response.json, 'email_rules')
		self.assertEqual(len(email_rules), 0)
		self.assertEqual(count, 0)

	def test_get_email_rules_returns_email_rules(self):
		mock_email_rule = EmailRule('foo', 'bar', 'baz')
		db.session.add(mock_email_rule)
		db.session.commit()
		response = self.client.get(url_for('api.get_email_rules'))
		self.assertEqual(response.status_code, 200)
		email_rules, count = self.get_list(response.json, 'email_rules')
		self.assertEqual(len(email_rules), count)
		self.assertEqual(count, 1)
		email_rule = email_rules[0]	
		for key in ['query', 'category', 'email_address']:
			email_rule_value = email_rule[key] 
			expected_value = getattr(mock_email_rule, key)
			self.assertEqual(email_rule_value, expected_value)

