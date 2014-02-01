from categories import categories
from moocha import db
from moocha.gumtree import Gumtree
from moocha.models import Advertisement
from categories import categories
from locations import locations


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
