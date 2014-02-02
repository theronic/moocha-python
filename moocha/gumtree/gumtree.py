import os
import json
from bs4 import BeautifulSoup
import mechanize
from urllib import urlencode
from advertisement import Advertisement
import logging
from moocha.utils import load_json, dump_json
logger = logging.getLogger(__name__)

class Gumtree(object):
	def __init__(self):
		logger.debug('Creating Gumtree object.')
		self.home_page_url = 'http://www.gumtree.co.za'
		self.search_url = 'http://www.gumtree.co.za/search.html'
		self.category_id_map = load_json(__file__, 'category_id_map.json')
		self.location_id_map = load_json(__file__, 'location_id_map.json')
		self.category_map = load_json(__file__, 'category_map.json')
		self.location_map = load_json(__file__, 'location_map.json')

	def search(self, query, category='All Categories', location='South Africa'):
		"""Search for ads on gumtree, returning the results as a list
		of elements of type gumtree.Advertisement.
		"""
		logger.debug('Searching for query:%s, category:%s, location:%s', query, category, location)
		catId = self.get_category_id(category)
		locId = self.get_location_id(location)
		# Build the search url, combining search terms and categories.
		url = '?'.join([self.search_url, urlencode({
			'q': query,
			'catId': catId,
			'locId': locId,
			})])
		# Get the page's contents.
		contents = self.get_page_contents(url)
		# Parse gumtree's response to the mechanize browser.
		soup = BeautifulSoup(contents)
		# Get Advertisement objects from the soup.
		return self.parse_search_results_page(soup)

	def bootstrap_maps(self):
		"""Write a default category and location map that just maps 1:1 between
		searcher categories and gumtree categories, and searcher locations and
		gumtree locations.
		"""
		# Import this here to avoid circular imports.
		from moocha import Searcher
		# Make a searcher instance to get the categories and locations from.
		searcher = Searcher()
		# Build the category and location maps.
		category_map = {category: category for category in searcher.categories}
		dump_json(category_map, __file__, 'category_map.json')
		location_map = {location: location for location in searcher.locations}
		dump_json(location_map, __file__, 'location_map.json')
		# Get the category and location id maps from gumtree.co.za.
		category_id_map = self.get_category_id_map_from_website()
		dump_json(category_id_map, __file__, 'category_id_map.json')
		location_id_map = self.get_location_id_map_from_website()
		dump_json(location_id_map, __file__, 'location_id_map.json')

	def get_category_id_map_from_website(self):
		"""Get a dict associating gumtree categories with their 'catId'.
		This data is still raw and not in the format used by Searcher.
		"""
		logger.warn("Getting categories from gumtree's website.")
		# Get the contents of the home page.
		home_page_contents = self.get_page_contents(self.home_page_url)
		logger.debug("Fetched gumtree's home page.")
		assert len(home_page_contents)
		# Parse the homepage using BeautifulSoup
		soup = BeautifulSoup(home_page_contents)
		# The js variable containing the categories.
		javascript_variable_name = 'CATEGORY_FILTER_JSON'
		# Get the script containing this variable.
		script = self.get_script_containing_variable(javascript_variable_name, soup)	
		# Get the value of this variable after assignment.
		categories_json = self.extract_assignments_value_from_javascript(
			variable_name=javascript_variable_name,
			javascript=script,
		)
		# Parse the categories into a dict.
		categories_dict = json.loads(categories_json)
		# Now flatten this dict into a dict associateing dot concatinated sub-
		# categories and their 'catId' and return it.
		return self.flatten_gumtree_select_dict(categories_dict)

	def get_category_id(self, searcher_category):
		"""Get the gumtree catId associated with a searcher category.
		"""
		assert searcher_category in self.category_map, "Searcher category '%s' doesn't correspond to any Gumtree category." % searcher_category
		# First get the gumtree category associated with the searcher category.
		gumtree_category = self.category_map[searcher_category]
		# Then return the catId associated with that category_name.
		assert gumtree_category in self.category_id_map, "Gumtree category '%s' doesn't correspond to any Gumtree CatId." % gumtree_category
		return self.category_id_map[gumtree_category]

	def get_location_id(self, searcher_location):
		"""Get the gumtree locId associated with a searcher location.
		"""
		assert searcher_location in self.location_map, "Searcher location '%s' doesn't correspond to any Gumtree location." % searcher_location
		# First get the gumtree location associated with the searcher location.
		gumtree_location = self.location_map[searcher_location]
		# Then return the catId associated with that location_name.
		assert gumtree_location in self.location_id_map, "Gumtree location '%s' doesn't correspond to any Gumtree locId." % gumtree_location
		return self.location_id_map[gumtree_location]

	def get_page_contents(self, url):
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


	def get_location_id_map_from_website(self):
		"""Get a dict associating gumtree's locations with their location id.
		"""
		logger.warn("Getting locations from gumtree's website.")
		# Get the contents of the home page.
		home_page_contents = self.get_page_contents(self.home_page_url)
		logger.debug("Fetched gumtree's home page.")
		assert len(home_page_contents)
		# Parse the homepage using BeautifulSoup.
		soup = BeautifulSoup(home_page_contents)
		# The name of the variable to scrape.
		javascript_variable_name = 'LOCATION_FILTER_JSON'
		# Get the script containing the variable name.
		script = self.get_script_containing_variable(javascript_variable_name, soup)
		# Extract the assignment of the javascript variable.
		locations_json = self.extract_assignments_value_from_javascript(
			variable_name=javascript_variable_name,
			javascript=script,
		)
		# Now parse this json into a dict.
		locations_dict = json.loads(locations_json)
		# Now flatten this dict into a dict associateing dot concatinated sub-
		# areas and their 'areaId' and return it.
		return self.flatten_gumtree_select_dict(locations_dict)
 
	def extract_assignments_value_from_javascript(self, variable_name, javascript):
		"""Given a snippet of javascript with an assignment,
		extract the value of the assignment, (extract the right
		hand side).
		"""
		# Next get the line of javascript containing our variable.
		line = next(line for line in javascript.split('\n') if variable_name in line)
		# Next strip away all but the right hand side of the assignment.
		return (line.replace('var ' + variable_name + ' = ', '')
			.replace(';', ''))

	def get_script_containing_variable(self, variable_name, soup):
		"""Return the string contents of a script element containing
		the given variable name.
		"""
		# Get the text for all the script elements in the target page.
		scripts = [str(script.string) for script in soup.find_all('script')]
		return next(script for script in scripts if variable_name in script)

	def flatten_gumtree_select_dict(self, all_elements):
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
