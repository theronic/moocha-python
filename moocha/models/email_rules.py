from moocha import db


notifications = db.Table('notifications', db.Model.metadata,
	db.Column('email_rule_id', db.Integer, db.ForeignKey('email_rules.id')),
	db.Column('advertisement_id', db.Integer, db.ForeignKey('advertisements.id')),
	)


class EmailRule(db.Model):
	__tablename__ = 'email_rules'
	id = db.Column(db.Integer, primary_key=True)

	# The email address to send new offers to.
	email_address = db.Column(db.String(256), unique=False, nullable=False)

	query = db.Column(db.String(256), unique=False, nullable=False)

	category = db.Column(db.String(256), unique=False, nullable=False)

	last_sent_on = db.Column(db.DateTime, unique=False, nullable=True)

	advertisements = db.relationship('Advertisement', secondary=notifications, backref='email_rules')

	def __init__(self, email_address, query, category):
		self.email_address = email_address
		self.query = query
		self.category = category

	def __repr__(self):
		return "<EmailRule: address:%s>" % self.email_address

	def to_dict(self):
		return {
			'category': self.category,
			'email_address': self.email_address,
			'query': self.query,
		}