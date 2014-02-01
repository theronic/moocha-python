import unittest
from advertisement import Advertisement
from moocha.utils import fuzz
from mock import patch
import bs4


class TestAdvertisement(unittest.TestCase):
	def test_to_dict(self):
		ad = Advertisement(fuzz(), fuzz(), fuzz())
		result = ad.to_dict()
		for attr in ['title', 'description', 'price']:
			self.assertEqual(result[attr], getattr(ad, attr))

	def test_from_search_listing(self):
		title = 'hello'
		description = 'world' 
		soup = bs4.BeautifulSoup("""
			<li class="result pictures">
				<div class="containter">
					<div class="title">
						<a>hello</a>
					</div>
					<div class="description hidden">
						world
					</div>
				</div>
			</li>
		""") 
		ad = Advertisement.from_search_listing(soup)
		self.assertEqual(ad.title, title)	
		#TODO: Implement html cleaner upper.
		self.assertEqual(ad.description.strip(), description)	
