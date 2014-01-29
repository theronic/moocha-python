import logging
logger = logging.getLogger(__name__)
from utils import determine_environment
from utils.configuration import Configuration

class MoochaConfig(Configuration):
	required_values = [
		'EMAILER_SOURCE_ADDRESS',
		'AWS_ACCESS_KEY_ID',
		'AWS_SECRET_KEY',
		'SQLALCHEMY_DATABASE_URI',
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