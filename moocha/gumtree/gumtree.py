from bs4 import BeautifulSoup
import mechanize
from urllib import urlencode
from categories import categories
from advertisement import Advertisement

class Gumtree(object):
	def __init__(self):
		self.home_page_url = 'http://www.gumtree.co.za'
		self.search_url = 'http://www.gumtree.co.za/search.html'
		self.categories = categories

	def get_categories_from_website(self):
		# Get the contents of the home page.
		home_page_contents = self.get_page_contents(self.home_page_url)
		soup = BeautifulSoup(home_page_contents)
		select = soup.find(class_='select')
		categories = dict() 
		for link in select.find_all('a'):
			_id = link.get('data-id')
			name = link.contents[0]
			categories[name] = _id
		return categories


	def get_page_contents(self, url):
		# Instantiate a mechanize browser to open the page, (makes
		# it easy to handle things like cookies and redirects).
		browser = mechanize.Browser()
		# Open the search url with the mechanize browser.
		browser.open(url)
		return browser.response().read()

	def parse_search_results_page(self, soup):
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


	def search(self, terms, category='All categories'):
		# Build the search url, combining search terms and categories.
		url = '?'.join([self.search_url, urlencode({
			'q': terms,
			'catId': self.categories[category],
			})])
		# Get the page's contents.
		contents = self.get_page_contents(url)
		# Parse gumtree's response to the mechanize browser.
		soup = BeautifulSoup(contents)
		# Get Advertisement objects from the soup.
		return self.parse_search_results_page(soup)
