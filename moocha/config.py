import logging
logger = logging.getLogger(__name__)

class Configuration(object):
	values = dict() 
	def validate(self, values, required_values):
		for value in required_values:
			assert value in values, 'Configuration missing required value: %s' % value

	def set_value(self, key, value):
		assert key in self.required_values
		self.values[key] = value

	def get(self, value):
		self.validate(self.values, self.required_values)
		assert value in self.required_values
		return self.values[value]

	def from_module(self, module):
		for value in dir(module):
			if value in self.required_values:
				self.set_value(value, getattr(module, value))

	def from_dict(self, d):
		for key, value in d.items():
			if key in self.required_values:
				self.set_value(key, value)


import os, sys

environments = ['CI', 'HEROKU', 'DEV', 'TESTING']

def determine_environment():
	environment = None
	if 'DYNO' in os.environ:
		environment = 'HEROKU'
	elif 'CI' in os.environ and os.environ['CI']:
		environment = 'CI'
	elif 'test' in sys.argv:
		environment = 'TESTING'
	else:
		environment = 'DEV'
	assert environment in environments
	return environment



class MoochaConfig(Configuration):
	required_values = [
		'EMAILER_SOURCE_ADDRESS',
		'AWS_ACCESS_KEY_ID',
		'AWS_SECRET_KEY',
		'SQLALCHEMY_DATABASE_URI',
		'RUN_INTEGRATION_TESTS',
	]

config = MoochaConfig()

environment = determine_environment()
logger.info('Running in %s mode.', environment)

if environment == 'DEV':
	import dev_config 
	config.from_module(dev_config)
elif environment == 'HEROKU':
	import os
	config.from_dict(os.environ)
elif environment == 'TESTING' or environment == 'CI':
	import test_config
	config.from_module(test_config)
else:
	raise ValueError('Environment not handled.')