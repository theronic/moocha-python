from categories import categories
from moocha import db, gumtree_instance
from moocha.gumtree import Gumtree
from moocha.models import Advertisement
from categories import categories
from locations import locations
import json
import os
import logging
logger = logging.getLogger(__name__)


class Searcher(object):
	backends = [Gumtree]
	locations = locations
	categories = categories
	def __init__(self):
		self.backends = [backend() for backend in self.backends]
		#TODO: Build categories calling each backend in turn.

	def get_categories(self):
		return list(categories)

	def get_locations(self):
		return list(locations)

	def search(self, query, category):
		"""Search on the different websites and colate the results.
		"""
		all_results = list()
		for backend in self.backends:
			backend_results = backend.search(query, category)
			results = [Advertisement.FromBackend(backend, result) for result in backend_results]
			all_results += results
		return all_results

	def bootstrap_categories_and_locations(self):
		logger.warn("Overwriting current searcher categories and"
			"locations with the latest categories and locations from Gumtree.")
		# Make a new gumtree instance to fetch the categories with.
		gumtree = gumtree_instance
		categories = list(gumtree.get_category_ids_from_website())
		assert len(categories), 'Got no categories from Gumtree.'
		locations = list(gumtree.get_location_ids_from_website())
		assert len(locations), 'Got no locations from Gumtree.'
		# Get the path of the categories file.
		categories_file = os.path.join(
			os.path.dirname(os.path.realpath(__file__)),
			'categories.json'
		)
		logger.debug('Writing categories to %s.', categories_file)
		with open(categories_file, 'w') as f:
			f.write(json.dumps(categories))
		# Get the path of the locations file.
		locations_file = os.path.join(
			os.path.dirname(os.path.realpath(__file__)),
			'locations.json'
		)
		logger.debug('Writing locations to %s.', locations_file)
		with open(locations_file, 'w') as f:
			f.write(json.dumps(locations))
