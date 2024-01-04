from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv
import os
# Load environment variables
load_dotenv()

def initDatabase():
    databaseUsername = os.getenv('SERVER_USERNAME')
    databasepassword = os.getenv('SERVER_PASS')
    uri = f"mongodb+srv://{databaseUsername}:{databasepassword}@cluster0.f24xmyu.mongodb.net/content_database?retryWrites=true&w=majority"
    client = MongoClient(uri, server_api=ServerApi('1'))
                            
    return client['content_database']
# This is added so that many files can reuse the function get_database()
if __name__ == "__main__":

    # Get the database
    dbname = initDatabase()