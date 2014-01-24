from categories import categories
import notify
from notify.gumtree import Gumtree
from advertisement import Advertisement


class Searcher(object):
	def __init__(self):
		self.backends = [Gumtree()]

	def get_categories(self):
		return list(categories)

	def search(self, search_terms, category):
		"""Search on the different websites and colate the results.
		"""
		all_results = list()
		for backend in self.backends:
			backend_results = backend.search(search_terms, category)
			results = [Advertisement.FromBackend(backend, result) for result in backend_results]
			all_results += results
		return all_results
