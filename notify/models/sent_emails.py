from notify import db


class SentEmail(db.Model):
	__tablename__ = 'sent_emails'
	id = db.Column(db.Integer, primary_key=True)

	email_address = db.Column(db.String(256))

	subject = db.Column(db.String(256))

	body = db.Column(db.String(4096))

	def to_dict(self):
		return {
			'email_address': self.email_address,
			'title': self.title,
			'subject': self.subject,
			'body': self.body,
		}