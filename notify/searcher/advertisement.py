class Advertisement(object):
	def __init__(self, title, description, source):
		self.title = title
		self.description = description
		self.source = source


	@staticmethod
	def FromGumtree(advertisement):
		return Advertisement(
			title=advertisement.title,
			description=advertisement.description,
			source='Gumtree'
		)

	@staticmethod
	def GetHandler(backend):
		handlers = {
			'Gumtree': Advertisement.FromGumtree,
		}
		return handlers[backend.__class__.__name__]

	@staticmethod
	def FromBackend(backend, advertisement):
		handler = Advertisement.GetHandler(backend)
		return handler(advertisement)

	def to_dict(self):
		return {
			'title': self.title,
			'description': self.description,
			'source': self.source,
		}