import sys
sys.path.append("Database")
from worth2watch.Database.DatabaseInitialization import initDatabase
def createCollection():

    # Get the database
    dbname = initDatabase()
    collection_name = dbname["movies"]
    return collection_name