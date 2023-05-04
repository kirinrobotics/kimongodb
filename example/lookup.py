from pymongo import MongoClient
import json
from bson import ObjectId

# Define a custom JSON encoder that converts ObjectId to string
class MongoEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)

ip_address = '127.0.0.1'
port = '27017'

# Connect to MongoDB
client = MongoClient(f'mongodb://{ip_address}:{port}/')

# Access the "users" and "orders" collections in the "mydatabase" database
db = client["mydatabase"]
users_collection = db["users"]
orders_collection = db["orders"]

# Define the pipeline for the aggregation query
pipeline = [
    {
        "$lookup": {
            "from": "orders",
            "localField": "_id",
            "foreignField": "user_id",
            "as": "orders"
        }
    },
    {
        "$sort": {"_id": 1}
    }
]

# Execute the aggregation query and convert the results to a list
results = list(users_collection.aggregate(pipeline))

# Write the results to a JSON file using the custom encoder
with open("mongodb/users_with_orders.json", "w") as f:
    json.dump(results, f, cls=MongoEncoder, indent=4)