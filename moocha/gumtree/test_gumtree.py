import unittest
import gumtree
from gumtree import Gumtree
from moocha import config
from mock import Mock
from moocha.utils import fuzz


class TestGumtree(unittest.TestCase):
	def setUp(self):
		self.gumtree = Gumtree()

	def test_search_builds_correct_url(self):
		# Return an empty string for bs4 to parse.
		self.gumtree.get_page_contents = Mock()
		gumtree.BeautifulSoup = Mock
		self.gumtree.parse_search_results_page = Mock()
		query = fuzz()
		category_name = fuzz()
		category_id = 0
		self.gumtree.categories = {category_name: category_id}
		expected_url = 'http://www.gumtree.co.za/search.html?q=%s&catId=0' % query
		self.gumtree.search(query=query, category=category_name)
		self.gumtree.get_page_contents.assert_called_with(expected_url)

	def test_search_calls_beautiful_soup(self):
		page_contents = fuzz()
		# Return an empty string for bs4 to parse.
		self.gumtree.get_page_contents = Mock(return_value=page_contents)
		self.gumtree.parse_search_results_page = Mock()
		category_name = fuzz()
		self.gumtree.categories = {category_name: 0}
		gumtree.BeautifulSoup = Mock()
		self.gumtree.search(query=fuzz(), category=category_name)
		gumtree.BeautifulSoup.assert_called_with(page_contents)

	def test_search_calls_parse_search_results(self):
		category_name = fuzz()
		self.gumtree.categories = {category_name: 0}
		self.gumtree.get_page_contents = Mock()	
		soup = gumtree.BeautifulSoup('')
		gumtree.BeautifulSoup  = Mock(return_value=soup)
		self.gumtree.parse_search_results_page = Mock()
		self.gumtree.search(fuzz(), category_name)
		self.gumtree.parse_search_results_page.assert_called_with(soup)

	def test_search_returns_parsed_search_results(self):
		category_name = fuzz()
		self.gumtree.categories = {category_name: 0}
		self.gumtree.get_page_contents = Mock()	
		gumtree.BeautifulSoup  = Mock()
		expected_search_result = fuzz()
		self.gumtree.parse_search_results_page = Mock(return_value=expected_search_result)
		search_result = self.gumtree.search(fuzz(), category_name)
		self.assertEqual(search_result, expected_search_result)


	def test_search(self):
		# Load the mock search result page.
		def get_page_contents(url):
			contents = open('moocha/gumtree/test_pages/search_result.html').read()
			return contents
		self.gumtree.get_page_contents = get_page_contents
		results = self.gumtree.search(fuzz())

	@unittest.skipIf(not config.get('RUN_INTEGRATION_TESTS'), "Not running integration tests.")
	def test_get_categories_from_website(self):
		categories = self.gumtree.get_categories_from_website()
		self.assertIsInstance(categories, dict)
		self.assertIn('All Categories.Property.Short Term', categories)

	@unittest.skipIf(not config.get('RUN_INTEGRATION_TESTS'), "Not running integration tests.")
	def test_get_locations_from_website(self):
		locations = self.gumtree.get_locations_from_website()
		self.assertIn('South Africa.Gauteng.Pretoria / Tshwane', locations)
