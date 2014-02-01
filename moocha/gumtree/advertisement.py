class Advertisement(object):
	def __init__(self, title, description, price):
		self.title = title
		self.description = description
		self.price = price

	def to_dict(self):
		return {
			'title': self.title,
			'description': self.description,
			'price': self.price
		}

	@staticmethod
	def from_search_listing(search_listing):
		title = Advertisement.extract_title_from_search_listing(search_listing)
		description = Advertisement.extract_description_from_search_listing(search_listing)
		price = Advertisement.extract_price_from_search_listing(search_listing)
		return Advertisement(
			title=title,
			description=description,
			price=price,
		)

	@staticmethod
	def extract_price_from_search_listing(search_listing):
		price_element = search_listing.find(class_='amount')
		if price_element:
			price_string = unicode(price_element.string)
			price_string = price_string.replace('R', '')
			price_string = price_string.replace(',', '')
			return int(price_string)

	@staticmethod
	def extract_title_from_search_listing(search_listing):
		return unicode(search_listing.find(class_='title').a.string)

	@staticmethod
	def extract_description_from_search_listing(search_listing):
		return unicode(search_listing.find(class_='description').string)