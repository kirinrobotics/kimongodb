from pymongo import MongoClient
import pymongo
import time
import json
from bson import ObjectId

ip_address = 'localhost'
port = '27017'

# Connect to MongoDB
client = MongoClient(f'mongodb://{ip_address}:{port}/')

# Access the "school" database and the "student" and "teacher" collections
db = client['school']
student_collection = db["Student"]
teacher_collection = db["Teacher"]

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

def poll_person_type():
    """
    Continuously polls the student and teacher collections for new objects and writes the
    corresponding data to a JSON file.

    Returns:
    None
    """
    last_person_type = None
    while True:
        # Find the most recent student and teacher in each collection
        latest_student = student_collection.find_one(sort=[("_id", pymongo.DESCENDING)])
        latest_teacher = teacher_collection.find_one(sort=[("_id", pymongo.DESCENDING)])
        
        # Get the person types from each collection
        student_type = latest_student.get("person_type") if latest_student else None
        teacher_type = latest_teacher.get("person_type") if latest_teacher else None
        
        # If the person type has changed, perform the aggregation query
        if student_type != last_person_type and student_type is not None:
            print("New student in Student collection: ", student_type)
            last_person_type = student_type
        elif teacher_type != last_person_type and teacher_type is not None:
            print("New teacher in Teacher collection: ", teacher_type)
            last_person_type = teacher_type
        time.sleep(5)

poll_person_type()