from bs4 import BeautifulSoup
from moocha.utils.skip_integration_tests import integration_test
import mechanize
from urllib import urlencode
from categories import categories
from advertisement import Advertisement
import logging
import json
logger = logging.getLogger(__name__)
from categories import categories
from locations import locations
from searcher_gumtree_category_map import searcher_gumtree_category_map
from searcher_gumtree_location_map import searcher_gumtree_location_map

class Gumtree(object):
	home_page_url = 'http://www.gumtree.co.za'
	def __init__(self):
		logger.debug('Creating Gumtree object.')
		self.search_url = 'http://www.gumtree.co.za/search.html'
		self.searcher_gumtree_category_map = searcher_gumtree_category_map
		self.searcher_gumtree_location_map = searcher_gumtree_location_map
		self.categories = categories
		self.locations = locations

	@staticmethod
	def serialize_dict_to_python_module(dict_, module_path, variable_name):
		with open(module_path, 'w') as f:
			f.write('%s = {\n' % variable_name)
			for key, value in dict_.items():
				f.write('"%s":"%s",\n' % (key, value))
			f.write('}\n')

	@staticmethod
	def BuildAndWriteSearcherBackendLocationMap(locations):
		import os
		path = os.path.join(os.path.dirname(os.path.realpath(__file__)),
			'searcher_gumtree_location_map.py')
		searcher_gumtree_location_map = {location: location.split('.')[-1] for location in locations}
		Gumtree.serialize_dict_to_python_module(searcher_gumtree_location_map,
			path,
			'searcher_gumtree_location_map',
		)

	@staticmethod
	def BuildAndWriteSearcherBackendCategoryMap(categories):
		import os
		path = os.path.join(os.path.dirname(os.path.realpath(__file__)),
			'searcher_gumtree_category_map.py')
		searcher_gumtree_category_map = {category: category.split('.')[-1] for category in categories}
		Gumtree.serialize_dict_to_python_module(searcher_gumtree_category_map,
			path,
			'searcher_gumtree_category_map',
		)

	def get_category_id(self, category):
		"""Get the gumtree catId associated with a searcher category.
		"""
		assert category in self.searcher_gumtree_category_map, "Category '%s' doesn't correspond to any Gumtree category." % category
		# First get the gumtree category associated with the searcher category.
		category_name = self.searcher_gumtree_category_map[category]
		# Then return the catId associated with that category_name.
		return self.categories[category_name]

	def get_location_id(self, location):
		assert location in self.searcher_gumtree_location_map, "Location '%s' doesn't correspond to any Gumtree location." % location
		# First get the gumtree location associated with the searcher location.
		location_name = self.searcher_gumtree_location_map[location]
		# Then return the catId associated with that location_name.
		return self.locations[location_name]

	def search(self, query, category='All Categories', location='South Africa'):
		"""Search for ads on gumtree, returning the results as a list
		of elements of type gumtree.Advertisement.
		"""
		logger.debug('Searching for query:%s, category:%s', query, category)
		catId = self.get_category_id(category)
		locId = self.get_location_id(location)
		# Build the search url, combining search terms and categories.
		url = '?'.join([self.search_url, urlencode({
			'q': query,
			'catId': catId,
			'locId': locId,
			})])
		print(url)
		# Get the page's contents.
		contents = self.get_page_contents(url)
		# Parse gumtree's response to the mechanize browser.
		soup = BeautifulSoup(contents)
		# Get Advertisement objects from the soup.
		return self.parse_search_results_page(soup)

	@staticmethod
	def get_page_contents(url):
		"""Fetch the raw contents of a web page (the html text).
		"""
		# Instantiate a mechanize browser to open the page, (makes
		# it easy to handle things like cookies and redirects).
		browser = mechanize.Browser()
		# Open the url with the mechanize browser.
		browser.open(url)
		# Return the data given the the mechanize browser.
		return browser.response().read()

	def parse_search_results_page(self, soup):
		"""Parse the search results page and return a list of gumtree.Advertisement
		elements as a result.
		"""
		list_view = soup.body.find('div', class_='list-view')
		if list_view is None:
			logger.debug('Parser found no results.')
			return []
		# Create a list to store the search results in.
		search_results = list()
		# Gumtree uses two classes, one for a listing with and one for a listing without
		# pictures, so we find all elements of each class.
		for class_ in ['result', 'result pictures']:
			# Get all the 'li' elements with the class.
			listings = list_view.find_all('li', class_=class_)
			# Parse each listing into a gumtree.Advertisement object.
			search_results += [Advertisement.from_search_listing(listing) for listing in listings]
		return search_results

	@staticmethod
	def GetCategoriesFromWebsite():
		"""Get a dict associating gumtree's categories with their 'catId'
		from gumtree's homepage.

		This data is still raw and not in the format used by Searcher.
		"""
		logger.warn("Getting categories from gumtree's website.")
		# Get the contents of the home page.
		home_page_contents = Gumtree.get_page_contents(Gumtree.home_page_url)
		logger.debug("Fetched gumtree's home page.")
		assert len(home_page_contents)
		# Parse the homepage using BeautifulSoup
		soup = BeautifulSoup(home_page_contents)
		# The js variable containing the categories.
		javascript_variable_name = 'CATEGORY_FILTER_JSON'
		# Get the script containing this variable.
		script = Gumtree.get_script_containing_variable(javascript_variable_name, soup)	
		# Get the value of this variable after assignment.
		categories_json = Gumtree.extract_assignments_value_from_javascript(
			variable_name=javascript_variable_name,
			javascript=script,
		)
		# Parse the categories into a dict.
		categories_dict = json.loads(categories_json)
		# Now flatten this dict into a dict associateing dot concatinated sub-
		# categories and their 'catId' and return it.
		return Gumtree.flatten_gumtree_select_dict(categories_dict)

	@staticmethod
	def GetLocationsFromWebsite():
		"""Get a dict associating gumtree's locations with their location id.
		"""
		logger.warn("Getting locations from gumtree's website.")
		# Get the contents of the home page.
		home_page_contents = Gumtree.get_page_contents(Gumtree.home_page_url)
		logger.debug("Fetched gumtree's home page.")
		assert len(home_page_contents)
		# Parse the homepage using BeautifulSoup.
		soup = BeautifulSoup(home_page_contents)
		# The name of the variable to scrape.
		javascript_variable_name = 'LOCATION_FILTER_JSON'
		# Get the script containing the variable name.
		script = Gumtree.get_script_containing_variable(javascript_variable_name, soup)
		# Extract the assignment of the javascript variable.
		locations_json = Gumtree.extract_assignments_value_from_javascript(
			variable_name=javascript_variable_name,
			javascript=script,
		)
		# Now parse this json into a dict.
		locations_dict = json.loads(locations_json)
		# Now flatten this dict into a dict associateing dot concatinated sub-
		# areas and their 'areaId' and return it.
		return Gumtree.flatten_gumtree_select_dict(locations_dict)
 
 	@staticmethod
	def extract_assignments_value_from_javascript(variable_name, javascript):
		"""Given a snippet of javascript with an assignment,
		extract the value of the assignment, (extract the right
		hand side).
		"""
		# Next get the line of javascript containing our variable.
		line = next(line for line in javascript.split('\n') if variable_name in line)
		# Next strip away all but the right hand side of the assignment.
		return (line.replace('var ' + variable_name + ' = ', '')
			.replace(';', ''))

	@staticmethod
	def get_script_containing_variable(variable_name, soup):
		"""Return the string contents of a script element containing
		the given variable name.
		"""
		# Get the text for all the script elements in the target page.
		scripts = [str(script.string) for script in soup.find_all('script')]
		return next(script for script in scripts if variable_name in script)

	@staticmethod
	def flatten_gumtree_select_dict(all_elements):
		"""Take a dict in gumtree's format for select dropdown
		and flatten it into a dot seperated dict associating
		the dot concatinated element names and their id.
		"""
		elements = dict()
		all_elements_name = all_elements['localizedName']
		elements[all_elements_name] = all_elements['id']
		for element in all_elements['children']:
			element_name = element['localizedName']
			elements['.'.join([all_elements_name, element_name])] = element['id']
			for sub_element in element['children']:
				sub_element_name = sub_element['localizedName']
				sub_element_id = sub_element['id']
				full_element_name = '.'.join([
					all_elements_name,
					element_name,
					sub_element_name,
				])
				elements[full_element_name] = sub_element_id
		return elements
