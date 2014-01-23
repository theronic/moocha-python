import unittest
from gumtree import Gumtree


class TestGumtree(unittest.TestCase):
	def setUp(self):
		self.gumtree = Gumtree()

	def test_search(self):
		# Load the mock search result page.
		def get_page_contents(url):
			contents = open('notify/gumtree/test_pages/search_result.html').read()
			return contents
		self.gumtree.get_page_contents = get_page_contents
		results = self.gumtree.search('hello')
		for result in results:
			print(result['description'])
		self.fail()
