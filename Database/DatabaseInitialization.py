from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv
import os
# Load environment variables
load_dotenv()
databaseUsername = os.getenv('SERVER_USERNAME')
databasepassword = os.getenv('SERVER_PASS')
print(databaseUsername, databasepassword.strip())
uri = f"mongodb+srv://{databaseUsername}:{databasepassword}@cluster0.f24xmyu.mongodb.net/?retryWrites=true&w=majority"

print(uri)
client = MongoClient(uri, server_api=ServerApi('1'))
                          
# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

