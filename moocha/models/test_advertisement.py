import unittest
from advertisement import Advertisement


class TestAdvertisement(unittest.TestCase):
	def test_equal_advertisements_compare_equal(self):
		a = Advertisement('foo', 'bar', 'gumtree')
		b = Advertisement('foo', 'bar', 'gumtree')

	def test_unequal_advertisements_compare_unequal(self):
		a = Advertisement('foo', 'bar', 'gumtree')
		b = Advertisement('boo', 'far', 'gumtree')
