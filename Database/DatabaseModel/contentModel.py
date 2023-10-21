import sys
sys.path.append("Database")
from DatabaseInitialization import initDatabase
from pymongo import MongoClient

def createCollection():
    # Get the database
    dbname = initDatabase()
    collection_name = dbname["movies"]
    return collection_name