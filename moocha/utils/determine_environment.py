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
