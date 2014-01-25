import unittest
from notify import create_app 
from notify.gumtree import Gumtree
import json

gumtree_instance = Gumtree()

class TestAPI(unittest.TestCase):
	def setUp(self):
		app = create_app()
		self.app = app.test_client()

	def test_status(self):
		result = json.loads(self.app.get('/api/status').data)
		# The success flag is present and True.
		self.assertIn('success', result)
		self.assertIsInstance(result['success'], bool)
		self.assertTrue(result['success'])
		# The message is present and is a string.
		self.assertIn('message', result)
		self.assertIsInstance(result['message'], basestring)

	@unittest.skip('Broken')
	def test_search(self):
		result = json.loads(self.app.get('/api/search?query=hello').data)
		pass
