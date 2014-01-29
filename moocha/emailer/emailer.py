import logging
import boto.ses
boto_logger = logging.getLogger('boto')
boto_logger.setLevel(logging.WARN)
from jinja2 import Environment, PackageLoader


class Emailer(object):
	def __init__(self, config):
		self.config = config
		self.conn = boto.ses.connect_to_region(
			'us-east-1',
			aws_access_key_id=self.config.get('AWS_ACCESS_KEY_ID'),
			aws_secret_access_key=self.config.get('AWS_SECRET_KEY'),
			)
		self.env = Environment(loader=PackageLoader('moocha.emailer', 'templates'))


	def send_email(self, address, subject_template_path, body_template_path, template_args=dict(), source_address=None):
		if source_address is None:
			source_address = self.config.get('EMAILER_SOURCE_ADDRESS')
		body_template = self.env.get_template(body_template_path)
		body = body_template.render(**template_args)
		subject_template = self.env.get_template(subject_template_path)
		subject = subject_template.render(**template_args)
		self.conn.send_email(
			source_address,
			subject,
			body,
			[address]
		)