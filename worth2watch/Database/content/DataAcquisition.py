import os
import requests
from bson import json_util
import dotenv
import sys
import datetime

from pymongo.errors import DuplicateKeyError
from worth2watch.Database.DatabaseModel.contentModel import createCollection as collection
from worth2watch.Database.content.providerCall import get_providers_with_retry
from worth2watch.Database.content.omdb_acquasition import get_movie_data
from worth2watch.agent_main.agent_main import main_agent


path_name = os.path.dirname(os.path.realpath(__file__))
sys.path.append(path_name)
global_counter =0

def is_valid(value, title):
    """
    Check if a value is valid.

    Args:
        value (any): The value to check.
        title (str): The title of the movie.

    Returns:
        bool: True if the value is valid, False otherwise.
    """
    print(f"Checking {value}...")
    print(value is not None and value != 'N/A')
    return value is not None and value != 'N/A'


def process_movie(contentObj, i):
    """
    Process a movie from the content object.

    Args:
        contentObj (dict): The content object.
        i (int): The index of the movie in the content object.

    Returns:
        dict or None: The processed movie data if successful, None otherwise.
    """
    movieTitle = contentObj["results"][i].get("title", "")
    movieId = contentObj["results"][i].get("id", "")
    try:
        release_date_str = contentObj["results"][i].get("release_date")
        movie_providers = get_providers_with_retry(movieId)
        if movie_providers is None:
            print(f"Error processing movie {movieTitle}: No providers returned")
            return None
        movie_data = get_movie_data(movieTitle)
        if movie_data is not None:
            if not is_valid(movie_data.get("score"), movieTitle):
                movie_data["score"] = [{"Source": "TMDB", "Value": contentObj['results'][i].get('vote_average')
                                        }]
            else:
                movie_data.setdefault("score", []).append({
                    "Source": "TMDB", "Value": contentObj['results'][i].get('vote_average')
                    })
            if all(is_valid(movie_data[key], movieTitle) for key in ["score", "poster_uri", "description", "runtime"]):
                global global_counter
                global_counter = global_counter + 1
                print("global_counter: ", global_counter)
                return {
                    "movieName": movieTitle,
                    "movieDescription": movie_data["description"],
                    "movieWriter": movie_data["writer"],
                    "movieActors": movie_data["actors"],
                    "movieGenres": movie_data["genres"],
                    "movieDirector": movie_data["director"],
                    "movieRuntime": movie_data["runtime"],
                    "movieScore": movie_data["score"],
                    "imageURL": movie_data["poster_uri"],
                    "movieReleaseDate": release_date_str,
                    "tmdbId": movieId,
                    "movieProvider": movie_providers if movie_providers is not None else None
                }
            else:
                print(f"Error processing movie {movieTitle}: Incomplete data")
        else:
            print(f"Error processing movie {movieTitle}: No data returned")
    except ValueError as e:
        # Handle the case when release_date is not a valid date
        print(f"Error processing release_date for movie {movieTitle}: {e}")
    return None

def accquireData():
    """
    Acquire data from the API and store it in the database.
    """
    dotenv.load_dotenv()
    authToken = os.getenv("AUTHORIZATION_TOKEN")
    databaseOBJ = []
    global global_counter
    import datetime
    pageNo = 1
    while global_counter != 400:
        current_datetime =datetime.datetime.now() - datetime.timedelta(days=30)
        current_datetime = current_datetime.strftime("%Y-%m-%d") 
        contentURI = f"https://api.themoviedb.org/3/discover/movie?include_adult=false&certification=PG|M&region=US&include_video=false&with_release_type=2|3|4&with_runtime.gte=80&with_original_language=en&page={pageNo}&primary_release_date.lte={current_datetime}&sort_by=primary_release_date.desc"
        headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {authToken}"
        }

        response = requests.get(contentURI, headers=headers)
        contentObj = response.json()

        for i in range(len(contentObj["results"])):
            print(i)
            movie_data = process_movie(contentObj, i)
            if movie_data is not None:
                databaseOBJ.append(movie_data)
        print("done with page ", pageNo, " total of viable movies ", global_counter)
        pageNo = pageNo + 1

    # Print the formatted data
    for data in databaseOBJ:
        try:
            # Attempt to insert the document
            collection("content").insert_one(data)
            print("Movie Name:", data["movieName"], "is added to the database\n")
            main_agent(movie_name=data['movieName'], reddit_status=True, youtube_status=True)
        except DuplicateKeyError:
            # Handle the case when a document with the same movieName already exists
            print("Error: Duplicate movieName -", data["movieName"], "Skipping...\n")
        except Exception as e:
            print(f"Error: {e}")


def get_popular_movies():
    """
    Get popular movies from the API and store them in the database.
    """
    dotenv.load_dotenv()
    authToken = os.getenv("AUTHORIZATION_TOKEN")
    print("@get_popular_movies")
    databaseOBJ = []

    if collection('popular_movies').count_documents({}) > 0:
        print("database is not empty")
        today = datetime.datetime.now()
        dbExpiryDate = collection('popular_movies').find_one(
            {"expiry_date": {"$exists": True}})
        if dbExpiryDate is not None:
            if dbExpiryDate["expiry_date"] > today:
                print("Popular movies are up to date")
                return
            else:
                print("Popular movies are not up to date")
                collection("popular_movies").drop()
                print("Popular movies are dropped")
                execute_movie_api(authToken, databaseOBJ)


def execute_movie_api(authToken, databaseOBJ):
    """
    Execute the movie API request and store the data in the database.

    Args:
        authToken (str): The authorization token.
        databaseOBJ (list): The list to store the movie data.
    """
    contentURI = "https://api.themoviedb.org/3/trending/movie/week?language=en-US"
    headers = {
                    "accept": "application/json",
                    "Authorization": f"Bearer {authToken}"
                }
    create_expiry_date = datetime.datetime.now() + datetime.timedelta(days=7)
    response = requests.get(contentURI, headers=headers)
    contentObj = response.json()

    for i in range(len(contentObj["results"])):
        movie_data = process_movie(contentObj, i)
        if movie_data is not None:
            movie_data["expiry_date"] = create_expiry_date
            databaseOBJ.append(movie_data)

    for data in databaseOBJ:
        try:
            collection("popular_movies").insert_one(data)
            collection("content").insert_one(data)
            main_agent(movie_name=data['movieName'], reddit_status=True, youtube_status=False)
            print("Movie Name:", data["movieName"], " is added to the database\n")
        except DuplicateKeyError:
            print("Error: Duplicate movieName -", data["movieName"], "Skipping...\n")
        except Exception as e:
            print(f"Error: {e}")