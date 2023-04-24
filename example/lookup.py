from pymongo import MongoClient
import json
from bson import ObjectId

# Define a custom JSON encoder that converts ObjectId to string
class MongoEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)

ip_adress = '192.168.1.139'
port = '27017'

# Connect to MongoDB
client = MongoClient(f'mongodb://{ip_adress}:{port}/')

# Access the "gimbal" collection in the "kirins" database
db = client['kirins']
gimbal_collection = db["Gimbal"]
gimbal_advance_collection = db["Gimbal Advance"]

# Define the pipeline for the aggregation query
pipeline = [
    {
        "$lookup": {
            "from": "Gimbal Advance",
            "localField": "gimbal_type",
            "foreignField": "type",
            "as": "gimbal_data"
        }
    }
]

# Execute the aggregation query and convert the results to a list
results = list(gimbal_collection.aggregate(pipeline))

# Write the results to a JSON file using the custom encoder
with open("kimongodb/gimbal_data.json", "w") as f:
    json.dump(results, f, cls=MongoEncoder, indent=4)
