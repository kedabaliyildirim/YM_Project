from pymongo import IndexModel, ASCENDING
from worth2watch.Database.DatabaseInitialization import initDatabase
import sys
sys.path.append("Database")

def createCollection(type):

    dbname = initDatabase()
    # Get the database
    dbname = initDatabase()

    if type == "content":
        collection_name = dbname["movies"]

        # Create a unique index on the movieName field
        index_model = IndexModel([("movieName", ASCENDING)], unique=True)
        collection_name.create_indexes([index_model])

        return collection_name
    elif (type == "admin"):
        collection_name = dbname["admin"]
        return collection_name
    elif (type == "users"):
        collection_name = dbname["users"]
        return collection_name
    elif (type == "popular_movies"):
        collection_name = dbname["popular_movies"]
        index_model = IndexModel([("movieName", ASCENDING)], unique=True)
        collection_name.create_indexes([index_model])
        return collection_name