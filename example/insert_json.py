import pymongo
import json

# Establish a connection to MongoDB
client = pymongo.MongoClient("mongodb://localhost:27017/")

# Select the database and collection to use
db = client["myschool"]
collection = db["student"]

# Load the data from the JSON file
with open('src/js/student.json') as f:
    data = json.load(f)

# Insert the data into the collection
result = collection.insert_many(data["students"])

# Print the IDs of the inserted documents
print(result.inserted_ids)
