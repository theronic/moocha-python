import unittest
from gumtree import Gumtree


class TestGumtree(unittest.TestCase):
	def setUp(self):
		self.gumtree = Gumtree()

	def test_search(self):
		# Load the mock search result page.
		def get_page_contents(url):
			contents = open('moocha/gumtree/test_pages/search_result.html').read()
			return contents
		self.gumtree.get_page_contents = get_page_contents
		results = self.gumtree.search('hello')

	@unittest.skip('temp')
	def test_get_categories_from_website(self):
		def get_page_contents(url):
			contents = open('moocha/gumtree/test_pages/home_page.html')
		#self.gumtree.get_page_contents = get_page_contents
		categories = self.gumtree.get_categories_from_website()
		self.fail()
