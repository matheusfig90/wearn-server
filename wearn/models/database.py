# Dependencies
from pymongo import MongoClient
from wearn import app

"""
	Database class
"""
class Database:

	"""
		Connect into database
	"""
	@staticmethod
	def connect():
		client = MongoClient(app.config['DB_HOST'])

		return client.wearn