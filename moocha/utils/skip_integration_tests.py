import unittest
from moocha import config

def integration_test(*args):
	return unittest.skip('Not running integration tests.')
