from pymongo import MongoClient
import pymongo
import time
import json
from bson import ObjectId

ip_adress = 'localhost'
port = '27017'

# Connect to MongoDB
client = MongoClient(f'mongodb://{ip_adress}:{port}/')

# Access the "gimbal" collection in the "kirins" database
db = client['kirins']
gimbal_collection = db["Gimbal"]
gimbal_advance_collection = db["Gimbal Advance"]

# Define a custom JSON encoder that converts ObjectId to string
class MongoEncoder(json.JSONEncoder):
	"""
	Custom JSON encoder to handle MongoDB objects.
	"""
	def default(self, o):
		"""
		Overrides the default JSON encoder to serialize MongoDB ObjectIds as strings.

		Args:
			o: The object to be serialized.

		Returns:
			If `o` is an instance of `pymongo.ObjectId`, its string representation is returned. Otherwise, the default
			JSON serialization is used.
		"""
		if isinstance(o, pymongo.ObjectId):
			return str(o)
		return super().default(o)

def poll_gimbal_type():
	"""
	Continuously polls the gimbal_collection for new gimbal types and writes the 
	corresponding gimbal data to a JSON file.

	Returns:
	None
	"""
	last_gimbal_type = None
	while True:
		# Find the most recent gimbal in the collection
		gimbal = gimbal_collection.find_one(sort=[("_id", pymongo.DESCENDING)])
		gimbal_type = gimbal.get("gimbal_type")
		# If the gimbal type has changed, perform the aggregation query
		if gimbal_type != last_gimbal_type:
			print("New gimbal type: ", gimbal_type) 
			last_gimbal_type = gimbal_type
		time.sleep(5)

poll_gimbal_type()