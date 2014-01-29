from moocha import db
import email_rules


class Advertisement(db.Model):
	__tablename__ = 'advertisements'
	id = db.Column(db.Integer, primary_key=True)

	title = db.Column(db.String(256))

	description = db.Column(db.String(1024))

	source = db.Column(db.String(256))

	def __init__(self, title, description, source):
		self.title = title
		self.description = description
		self.source = source

	def __eq__(self, other):
		for attr in ['title', 'description']:
			if getattr(self, attr) != getattr(other, attr):
				return False
		return True

	def __repr__(self):
		return "<Ad title='%s'>" % (self.title)

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