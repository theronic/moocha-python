from notify import db


class EmailRule(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	# The email address to send new offers to.
	email_address = db.Column(db.String(256), unique=False, nullable=False)

	query = db.Column(db.String(256), unique=False, nullable=False)

	category = db.Column(db.String(256), unique=False, nullable=False)

	last_sent = db.Column(db.DateTime, unique=False, nullable=True)

	def __init__(self, email_address, query, category):
		self.email_address = email_address
		self.query = query
		self.category = category

	def __repr__(self):
		return "<EmailRule: address:%s>" % self.email_address