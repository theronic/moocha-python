import unittest
from manage import manager


class TestManage(unittest.TestCase):
	def assert_command_in_manager(self, command, manager):
		self.assertIn(command, manager._commands)

	def test_commands_present(self):
		self.assert_command_in_manager('shell', manager)
		self.assert_command_in_manager('create_all', manager)
		self.assert_command_in_manager('send_emails', manager)
		self.assert_command_in_manager('test', manager)
		self.assert_command_in_manager('integration_test', manager)
		self.assert_command_in_manager('bootstrap_categories_and_locations', manager)
		self.assert_command_in_manager('bootstrap_gumtree_maps', manager)

