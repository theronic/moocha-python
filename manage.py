from flask_script import Manager, Shell
from moocha import create_app, sender_instance, db, gumtree_instance, searcher_instance
from moocha.gumtree import Gumtree
from moocha import models
import nose
import logging
import os

logger = logging.getLogger('manage')
logger.setLevel(logging.DEBUG)

app = create_app()

manager = Manager(app)

def make_shell_context():
	return dict(
		app=app,
		gt=gumtree_instance,
		models=models,
		db=db,
	)

manager.add_command('shell', Shell(make_context=make_shell_context))

@manager.command
def create_all():
	db.create_all()

@manager.command
def send_emails():
	sender_instance.process_email_rules()

@manager.command
def test():
	nose.main(argv=['moocha', '--failed'])

@manager.command
def integration_test():
	from moocha import config
	config.values['RUN_INTEGRATION_TESTS'] = True
	logger.warn('Running in DEV mode since integration requires live stuffs.')
	nose.main(argv=['moocha', '--failed'])

def serialize_list_to_python_module(list_, module_path, variable_name):
	with open(module_path, 'w') as f:
		f.write('%s = [\n' % variable_name)
		for item in list_:
			f.write('"%s",\n' % item)
		f.write(']\n')
	#TODO: Reimport this file and check that the categories are the same.

@manager.command
def bootstrap_categories_and_locations():
	searcher_instance.bootstrap_categories_and_locations()

@manager.command
def bootstrap_gumtree_maps():
	"""Build a default gumtree category to searcher category and
	gumtree location to searcher location map.
	"""
	gumtree_instance.bootstrap_maps()

#TODO: Implement a dev command which runs create_all and then runs the server.

def main():
	manager.run()

if __name__ == '__main__':
	main()
