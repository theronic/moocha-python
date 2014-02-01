import unittest
import gumtree
from gumtree import Gumtree
from gumtree import Advertisement
from moocha import config
from mock import Mock, patch
from moocha.utils import fuzz, integration_test
import mechanize
import bs4


class TestGumtree(unittest.TestCase):
	def setUp(self):
		self.gumtree = Gumtree()

	def test_parse_search_results_page_handles_no_results(self):
		soup = bs4.BeautifulSoup("""
			<html>
				<body>
				</body>
			</html>
		""")
		ads = self.gumtree.parse_search_results_page(soup)
		self.assertEqual(ads, [])

	def test_parse_search_results_page_calls_from_search_listing(self):
		soup = bs4.BeautifulSoup("""
			<html>
				<body>
					<div class="list-view">
						<div class="view"
							<ul>
								<li class="result">
								</li>
							</ul>
						</div>
					</div>
				</body>
			</html>
		""")
		with patch('moocha.gumtree.advertisement.Advertisement.from_search_listing') as from_search_listing:
			self.gumtree.parse_search_results_page(soup)
			search_listing = from_search_listing.call_args
			self.assertIsNotNone(search_listing.find(class_="result"))


	def test_get_page_contents_instantiates_mechanize_browser(self):
		gumtree.mechanize.Browser = Mock()
		self.gumtree.get_page_contents(fuzz())
		gumtree.mechanize.Browser.assert_called_with()

	def test_get_page_contents_calls_browser_open(self):
		mock_browser = Mock()
		mock_browser.open = Mock()
		gumtree.mechanize.Browser = Mock(return_value=mock_browser)
		url = fuzz()
		self.gumtree.get_page_contents(url)
		mock_browser.open.assert_called_with(url)

	def test_get_page_contents_returns_browsers_response(self):
		expected_response = fuzz()
		mock_response = Mock()
		mock_response.read = Mock(return_value=expected_response)
		mock_browser = Mock()
		mock_browser.response = Mock(return_value=mock_response)
		gumtree.mechanize.Browser = Mock(return_value=mock_browser)
		response = self.gumtree.get_page_contents(fuzz())
		mock_response.read.assert_called_with()
		self.assertEqual(response, expected_response)

	def test_search_builds_correct_url(self):
		# Return an empty string for bs4 to parse.
		self.gumtree.get_page_contents = Mock()
		with patch('moocha.gumtree.gumtree.BeautifulSoup'):
			self.gumtree.parse_search_results_page = Mock()
			query = fuzz()
			category_id = 0
			location_id = 0
			self.gumtree.get_category_id = Mock(return_value=category_id)
			self.gumtree.get_location_id = Mock(return_value=location_id)
			expected_url = 'http://www.gumtree.co.za/search.html?q=%s&locId=0&catId=0' % query
			self.gumtree.search(query=query, category='All Categories')
			self.gumtree.get_page_contents.assert_called_with(expected_url)

	def test_search_calls_beautiful_soup(self):
		page_contents = fuzz()
		# Return an empty string for bs4 to parse.
		self.gumtree.get_page_contents = Mock(return_value=page_contents)
		self.gumtree.get_category_id = Mock()
		self.gumtree.get_location_id = Mock()
		self.gumtree.parse_search_results_page = Mock()
		with patch('moocha.gumtree.gumtree.BeautifulSoup'):
			self.gumtree.search(query=fuzz(), category='All Categories')
			gumtree.BeautifulSoup.assert_called_with(page_contents)

	def test_search_calls_parse_search_results(self):
		self.gumtree.get_category_id = Mock()
		self.gumtree.get_location_id = Mock()
		self.gumtree.get_page_contents = Mock()	
		soup = bs4.BeautifulSoup('')
		with patch('moocha.gumtree.gumtree.BeautifulSoup', new=Mock(return_value=soup)):
			self.gumtree.parse_search_results_page = Mock()
			self.gumtree.search(fuzz(), 'All Categories')
			self.gumtree.parse_search_results_page.assert_called_with(soup)

	def test_search_returns_parsed_search_results(self):
		category_name = fuzz()
		self.gumtree.get_category_id = Mock()
		self.gumtree.get_location_id = Mock()
		self.gumtree.get_page_contents = Mock()	
		gumtree.BeautifulSoup  = Mock()
		expected_search_result = fuzz()
		self.gumtree.parse_search_results_page = Mock(return_value=expected_search_result)
		search_result = self.gumtree.search(fuzz(), category_name)
		self.assertEqual(search_result, expected_search_result)


	def test_search_end_to_end(self):
		with open('moocha/gumtree/test_pages/search_result.html') as search_result_page:
			self.gumtree.get_page_contents = Mock(return_value=search_result_page.read())
			results = self.gumtree.search(fuzz())

	def test_get_categories_from_website(self):
		page_contents = None
		with open('moocha/gumtree/test_pages/index.html') as f:
			page_contents = f.read()
		self.gumtree.get_page_contents = Mock(return_value=page_contents)
		categories = self.gumtree.GetCategoriesFromWebsite()
		self.assertIn('All Categories.Property.Short Term', categories)
		self.assertEqual(categories['All Categories.Property.Short Term'], 9001)

	@integration_test()
	def test_get_categories_from_website_integration(self):
		categories = self.gumtree.get_categories_from_website()
		self.assertIsInstance(categories, dict)
		self.assertIn('All Categories.Property.Short Term', categories)

	def test_get_locations_from_website(self):
		page_contents = None
		with open('moocha/gumtree/test_pages/index.html') as f:
			page_contents = f.read()
		self.gumtree.get_page_contents = Mock(return_value=page_contents)
		locations = self.gumtree.GetLocationsFromWebsite()
		self.assertIn('South Africa.Gauteng.Pretoria / Tshwane', locations)
		self.assertEqual(locations['South Africa.Gauteng.Pretoria / Tshwane'], 3100094)

	@integration_test()
	def test_get_locations_from_website_integration(self):
		locations = self.gumtree.GetLocationsFromWebsite()
		self.assertIn('South Africa.Gauteng.Pretoria / Tshwane', locations)

	def test_extract_assignments_value_from_javascript(self):
		expected_result = fuzz()
		result = self.gumtree.extract_assignments_value_from_javascript(
			'hello',
			"""var hello = '%s'""" % expected_result
		)
		self.assertEqual(eval(result), expected_result)
