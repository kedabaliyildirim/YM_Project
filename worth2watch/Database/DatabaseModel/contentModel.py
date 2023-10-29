import sys
sys.path.append("Database")
from worth2watch.Database.DatabaseInitialization import initDatabase
def createCollection(type):

    dbname = initDatabase()
    # Get the database
    if(type == "content"):
        collection_name = dbname["movies"]
        return collection_name
    elif(type == "admin"):
        collection_name = dbname["admin"]
        return collection_name
    elif(type == "users"):
        collection_name = dbname["users"]
        return collection_name