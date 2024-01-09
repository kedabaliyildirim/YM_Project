from worth2watch.Database.DatabaseModel.contentModel import createCollection as collection
from bson import json_util
from bson.objectid import ObjectId
# from worth2watch.Database.content.DataAcquisition import get_popular_movies
import json
from pymongo import DESCENDING, ASCENDING
import datetime
# Sample movie information
movie_info = {
    "movieName": "Wizards of the Lost Kingdom II",
    "movieDescription": "Three kingdoms have been overtaken by three evil lords and only a teen…",
    "movieWriter": "Charles B. Griffith, Lance Smith",
    "movieActors": "Mel Welles, Bobby Jacoby, David Carradine",
    "movieGenres": "Action, Fantasy, Adventure",
    "movieDirector": "Charles B. Griffith",
    "movieRuntime": "80 min",
    "movieScore": [5, 2],
    "imageURL": "https://m.media-amazon.com/images/M/MV5BYWNjZDkxZWYtYWEyNi00YWQ2LTk1Mz…",
    "movieReleaseDate": "1989-03-01",
    "tmdbId": 7237,
    "movieProvider": None,
    "comments": {},
    "redditComments": [],
    "youtubeComments": []
}

def create(movie_info):
    try:
        # Insert movie information
        collection('test').insert_one(movie_info)
        return True
    except Exception as e:
        print("Create Error:", e)
        return False

def read(movie_name):
    try:
        # Read a specific movie
        result = collection('test').find_one({"movieName": movie_name})
        if result:
            return True
        else:
            print("Read Result: Movie not found.")
            return False
    except Exception as e:
        print("Read Error:", e)
        return False

def update(movie_name, updated_info):
    try:
        # Update information of a specific movie
        collection('test').update_one({"movieName": movie_name}, {"$set": updated_info})
        return True
    except Exception as e:
        print("Update Error:", e)
        return False

def delete(movie_name):
    try:
        # Delete a specific movie
        collection('test').delete_one({"movieName": movie_name})
        # print("Delete Result: Movie deleted successfully.")
        return True
    except Exception as e:
        print("Delete Error:", e)
        return False

# Test functions
def test_main():
    try:
        creation =create(movie_info)
        reading = read("Wizards of the Lost Kingdom II")

        # Updated information
        updated_info = {
            "movieRuntime": "90 min",
        }

        updating =update("Wizards of the Lost Kingdom II", updated_info)

        deleting = delete("Wizards of the Lost Kingdom II")
        read("Wizards of the Lost Kingdom II")
        test_results = [creation, reading, updating, deleting]
        return test_results
    except Exception as e:
        print("Failed", e)
        return None