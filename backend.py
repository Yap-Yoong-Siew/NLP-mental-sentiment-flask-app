from dotenv import load_dotenv
import pymongo
import os
import json

load_dotenv()

client = pymongo.MongoClient(os.environ.get('MONGODB_CLIENT'))

db = client['dblecturer']

with open('db.json') as f:
	data = json.load(f)

#collection
# chapters_collection = db['chapters']
# # chapters_collection.insert_one(data)

# # #insert
# # # chapters_collection.insert_one({ "name": "John", "address": "Highway 37" })

# # #read
# data = chapters_collection.find_one({})
# print(data['What do you want to know about Database subject?'])

