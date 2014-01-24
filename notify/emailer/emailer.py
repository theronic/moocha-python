import boto.ses
from jinja2 import Environment, PackageLoader


class Emailer(object):
	def __init__(self, app):
		self.app = app
		self.conn = boto.ses.connect_to_region(
			'us-east-1',
			aws_access_key_id=self.app.config['AWS_ACCESS_KEY_ID'],
			aws_secret_access_key=self.app.config['AWS_SECRET_KEY'],
			)
		self.env = Environment(loader=PackageLoader('notify.emailer', 'templates'))


	def send_email(self, address, subject, template_path, values, source_address=None):
		template = self.env.get_template(template_path)
		if source_address is None:
			source_address = self.app.config['EMAILER_SOURCE_ADDRESS']
		body = template.render(**values)
		self.conn.send_email(
				source_address,
				subject,
				body,
				[address]
			)