from bs4 import BeautifulSoup
import mechanize
from urllib import urlencode
from categories import categories
from advertisement import Advertisement
import logging
import json
logger = logging.getLogger(__name__)

class Gumtree(object):
	def __init__(self):
		logger.debug('Creating Gumtree object.')
		self.home_page_url = 'http://www.gumtree.co.za'
		self.search_url = 'http://www.gumtree.co.za/search.html'
		self.categories = categories

	def search(self, query, category='All categories'):
		"""Search for ads on gumtree, returning the results as a list
		of elements of type gumtree.Advertisement.
		"""
		logger.debug('Searching for query:%s, category:%s', query, category)
		category_id = self.categories[category]
		# Build the search url, combining search terms and categories.
		url = '?'.join([self.search_url, urlencode({
			'q': query,
			'catId': category_id,
			})])
		# Get the page's contents.
		contents = self.get_page_contents(url)
		# Parse gumtree's response to the mechanize browser.
		soup = BeautifulSoup(contents)
		# Get Advertisement objects from the soup.
		return self.parse_search_results_page(soup)

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
		body = soup.body
		viewport = body.find(class_='viewport')
		containment = body.find(class_='containment')
		page = body.find(class_='page')
		content = body.find(class_='content')
		section = content.section
		wrap = section.find(class_='wrap')
		results_list_view = wrap.find(class_='results')
		if results_list_view is None:
			return []
		results = list()
		# Listings without pictures.
		for result in results_list_view.find_all('li', class_='result'):
			results.append(Advertisement(
				title=unicode(result.find(class_='title').a.contents[0]),
				description=unicode(result.find(class_='description').contents[0]),
			))
		# Listings with pictures.
		for result in results_list_view.find_all('li', class_='result pictures'):
			results.append(Advertisement(
					title=unicode(result.find(class_='title').a.contents[0]),
					description=unicode(result.find(class_='description').contents[0]),
			))
		return results

	def get_categories_from_website(self):
		"""Get a dict associating gumtree's categories with their id
		from gumtree's homepage.

		This data is still raw and not in the form used by Searcher.
		"""
		logger.warn("Getting categories from gumtree's website.")
		# Get the contents of the home page.
		home_page_contents = self.get_page_contents(self.home_page_url)
		logger.info("Fetched gumtree's home page.")

		assert len(home_page_contents), "Got no data fetching gumtree's homepage."
		soup = BeautifulSoup(home_page_contents)

		categories = dict()	

		script = [script.string for script in soup.find_all('script') if 'CATEGORY_FILTER_JSON' in str(script.string)][0]
		start_filter = 'CATEGORY_FILTER_JSON = '
		start = script.find(start_filter)
		end = script.find('var CATEGORY_FILTER_TITLES')
		category_json = script[start + len(start_filter):end].replace(';', '')
		top_category = json.loads(category_json)
		top_category_name = top_category['localizedName']
		for middle_category in top_category['children']:
			middle_category_name = middle_category['localizedName']
			for bottom_category in middle_category['children']:
				bottom_category_name = bottom_category['localizedName']
				id_ = bottom_category['id']
				category_name = '.'.join([top_category_name, middle_category_name, bottom_category_name])
				categories[category_name] = id_				

		return categories

	def get_locations_from_website(self):
		"""Get a dict associating gumtree's locations with their location id.
		"""
		logger.warn("Getting locations from gumtree's website.")
		# Get the contents of the home page.
		home_page_contents = self.get_page_contents(self.home_page_url)
		logger.info("Fetched gumtree's home page.")
		assert len(home_page_contents), "Got no data fetching gumtree's homepage."
		soup = BeautifulSoup(home_page_contents)
		location_filter_select = soup.find(class_='location-filter')
		assert location_filter_select, "Could not find select element on gutree's home page."
		# Create a dict to store the locations and their ids in.
		locations = dict() 

		script = [str(script.string) for script in soup.find_all('script') if 'LOCATION_FILTER_JSON' in str(script.string)][0]
		start_filter = 'LOCATION_FILTER_JSON = '
		start = script.find(start_filter)		
		end = script.find(';', start)

		locations_json = script[start + len(start_filter): end]

		top_location = json.loads(locations_json)
		top_location_name = top_location['localizedName']
		for middle_location in top_location['children']:
			middle_location_name = middle_location['localizedName']
			for bottom_location in middle_location['children']:
				bottom_location_name = bottom_location['localizedName']
				id_ = bottom_location['id']
				location_name = '.'.join([top_location_name, middle_location_name, bottom_location_name])
				locations[location_name] = id_				

		return locations  
