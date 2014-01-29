class Configuration(object):
	values = dict() 
	def validate(self, values, required_values):
		for value in required_values:
			assert value in values, 'Configuration missing required value: %s' % value

	def set_value(self, key, value):
		assert key in self.required_values
		self.values[key] = value

	def get(self, value):
		self.validate(self.values, self.required_values)
		assert value in self.required_values
		return self.values[value]

	def from_module(self, module):
		for value in dir(module):
			if value in self.required_values:
				self.set_value(value, getattr(module, value))

	def from_dict(self, d):
		for key, value in d.items():
			if key in self.required_values:
				self.set_value(key, value)
