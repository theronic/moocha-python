from bs4 import BeautifulSoup
import mechanize
from urllib import urlencode

class Gumtree(object):
	def __init__(self):
		self.search_url = 'http://www.gumtree.co.za/search.html'

		self.categories = {
			'all_categories': '',
			'automotive_vehicles': 5,
			'property': 2,
			'jobs': 8,
			'job_seekers': 9389,
			'services': 9,
			'home_and_garden': 9175,
			'electronics': 9178,
			'baby_and_kids': 9176,
			'boats_and_watercraft': 9101,
			'business_to_business': 9171,
			'fasion': 9177,
			'pets': 9122,
			'sports_and_leisure': 9179,
			'community': 6,
			'events': 9067,
		}

	def get_page_contents(self, url):
		# Instantiate a mechanize browser to open the page, (makes
		# it easy to handle things like cookies and redirects).
		browser = mechanize.Browser()
		# Open the search url with the mechanize browser.
		browser.open(url)
		return browser.response().read()

	def search(self, terms, category='all_categories'):
		# Build the search url, combining search terms and categories.
		url = '?'.join([self.search_url, urlencode({
			'q': terms,
			'catId': self.categories[category],
			})])
		# Get the page's contents.
		contents = self.get_page_contents(url)
		# Parse gumtree's response to the mechanize browser.
		soup = BeautifulSoup(contents)
		body = soup.body
		viewport = body.find(class_='viewport')
		containment = body.find(class_='containment')
		page = body.find(class_='page')
		content = body.find(class_='content')
		section = content.section
		wrap = section.find(class_='wrap')
		results_list_view = wrap.find(class_='results')
		results = list()
		# Listings without pictures.
		for result in results_list_view.find_all('li', class_='result'):
			results.append({
					'description': str(result.find(class_='description').contents),
					'title': str(result.find(class_='title').a.contents),
				})
		# Listings with pictures.
		for result in results_list_view.find_all('li', class_='result pictures'):
			results.append({
					'description': str(result.find(class_='description').contents),
					'title': str(result.find(class_='title').a.contents),
				})
		return results
