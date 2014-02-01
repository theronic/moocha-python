from flask_script import Manager, Shell
from moocha import create_app, sender_instance, db
from moocha.gumtree import Gumtree
from moocha import searcher 
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
		gt=Gumtree(),
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
	nose.main(argv=['moocha --failed'])

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
	logger.warn("Overwriting the list of categories with the current categories from Gumtree.")
	searcher_file = searcher.__file__
	searcher_directory = os.path.dirname(os.path.realpath(searcher_file))
	categories_file_path = os.path.join(searcher_directory, 'categories.py')
	categories = Gumtree.GetCategoriesFromWebsite()
	assert len(categories)
	logger.info("Got %d categories.", len(categories))
	logger.info("Writing categories to %s", categories_file_path)
	serialize_list_to_python_module(categories,
		categories_file_path,
		'categories'
	)
	logger.warn("Overwriting the list of locations with the current locations from Gumtree.")
	locations_file_path = os.path.join(searcher_directory, 'locations.py')
	locations = Gumtree.GetLocationsFromWebsite()
	assert len(locations)
	serialize_list_to_python_module(locations,
		locations_file_path,
		'locations',
	)

@manager.command
def build_and_write_backend_maps():
	categories = searcher.categories.categories
	locations = searcher.locations.locations
	backends = searcher.Searcher.backends
	for backend in backends:
		backend.BuildAndWriteSearcherBackendCategoryMap(categories)
		backend.BuildAndWriteSearcherBackendLocationMap(locations)

#TODO: Implement a dev command which runs create_all and then runs the server.

def main():
	manager.run()

if __name__ == '__main__':
	main()
