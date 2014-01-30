import unittest
from moocha import config
from jinja2 import Template
from emailer import Emailer
from mock import Mock
from moocha.models import EmailRule
from moocha.utils import fuzz


class TestEmailer(unittest.TestCase):
	def setUp(self):
		self.emailer = Emailer(config)

	def test_emailer_uses_correct_templates(self):
		mock_template = Template(fuzz())
		self.emailer.env.get_template = Mock(return_value=mock_template)
		self.emailer.conn.send_email = Mock()
		subject_template_path = fuzz()
		body_template_path = fuzz()
		self.emailer.send_email(fuzz(),
			subject_template_path=subject_template_path,
			body_template_path=body_template_path,
			source_address=fuzz(),
		)
		self.emailer.env.get_template.assert_any_calls(subject_template_path)
		self.emailer.env.get_template.assert_any_calls(body_template_path)

	def test_emailer_renders_templates_with_correct_arguments(self):
		mock_template = Mock(wraps=Template('.'))
		self.emailer.env.get_template = Mock(return_value=mock_template)
		self.emailer.conn.send_email = Mock()
		mock_template_args = {fuzz(): fuzz()}
		self.emailer.send_email(fuzz(),
			subject_template_path=fuzz(),
			body_template_path=fuzz(),
			source_address=fuzz(),
			template_args=mock_template_args,
		)
		mock_template.render.assert_called_with(**mock_template_args)

	def test_emailer_calls_boto_send_mail_correctly(self):
		mock_template = Template(fuzz())
		mock_template_value = fuzz() 
		mock_template.render = Mock(return_value=mock_template_value)
		self.emailer.env.get_template = Mock(return_value=mock_template)
		self.emailer.conn.send_email = Mock()
		mock_template_args = {fuzz(): fuzz()}
		mock_address = fuzz() + '@' + fuzz() + '.com'
		mock_source_address = fuzz() + '@' + fuzz() + '.com'
		self.emailer.send_email(mock_address,
			subject_template_path=fuzz(),
			body_template_path=fuzz(),
			source_address=mock_source_address,
			template_args=mock_template_args,
		)
		self.emailer.conn.send_email.assert_called_with(
			source=mock_source_address,
			body=mock_template_value,
			subject=mock_template_value,
			to_addresses=[mock_address]
		)

	@unittest.skipIf(config.get('RUN_INTEGRATION_TESTS') is not True, "Not running integration tests.")
	def test_end_to_end(self):
		"""Test that sending an email with boto does not throw any
		errors.
		"""
		self.emailer.send_email('avoid3d+test@gmail.com',
			subject_template_path='new_matching_ads_update/subject.html',
			body_template_path='new_matching_ads_update/body.html',
			source_address='avoid3d@gmail.com',
			template_args=dict(
				email_rule=EmailRule('', '', ''),
			),
		)
