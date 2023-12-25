import os
import requests
from bson import json_util
import dotenv
import sys
import datetime
from pymongo.errors import DuplicateKeyError
from worth2watch.Database.DatabaseModel.contentModel import createCollection as collection
from worth2watch.Database.content.providerCall import getProvidersWithRetry
from worth2watch.Database.content.omdb_acquasition import get_movie_data


path_name = os.path.dirname(os.path.realpath(__file__))
sys.path.append(path_name)


def is_valid(value, title):
    print(f"Checking if {value} is valid for {title}")
    print(value is not None and value != 'N/A')
    return value is not None and value != 'N/A'


def accquireData(year):
    dotenv.load_dotenv()
    authToken = os.getenv("AUTHORIZATION_TOKEN")

    databaseOBJ = []

    for i in range(1, 4):
        avarage = (i * 2) - 1
        contentURI = f"https://api.themoviedb.org/3/discover/movie?include_adult=false&include_video=false&page=1&sort_by=vote_count.desc&vote_average.lte={average}&year={year}"


        headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {authToken}"
        }

        response = requests.get(contentURI, headers=headers)
        contentObj = response.json()

        for i in range(len(contentObj["results"])):
            movieTitle = contentObj["results"][i].get("title", "")
            movieId = contentObj["results"][i].get("id", "")
            try:
                release_date_str = contentObj["results"][i].get("release_date")
                if release_date_str:
                    release_date = datetime.datetime.strptime(
                        release_date_str, "%Y-%m-%d").date()
                    if release_date < datetime.date.today():
                        movie_providers = getProvidersWithRetry(movieId)
                        movie_data = get_movie_data(movieTitle)
                        if movie_data is not None:
                            print(movie_data.get("score", ""))
                            print(movieTitle)
                            if not is_valid(movie_data.get("score"), movieTitle):
                                movie_data["score"] = [{
                                    "Source": "TMDB",
                                    "Value": contentObj['results'][i].get('vote_average')
                                }]

                            else:
                                movie_data.setdefault("score", []).append({
                                    "Source": "TMDB",
                                    "Value": contentObj['results'][i].get('vote_average')
                                })
                            if all(is_valid(movie_data[key], movieTitle) for key in ["score", "poster_uri", "description", "runtime"]):
                                databaseOBJ.append({
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
                                })
                            else:
                                print(f"Error processing movie {movieTitle}: Incomplete data")
                        else:
                            print(f"Error processing movie {movieTitle}: No data returned")
            except ValueError as e:
                # Handle the case when release_date is not a valid date
                print(f"Error processing release_date for movie {movieTitle}: {e}")

    # Print the formatted data
    for data in databaseOBJ:
        try:
            # Attempt to insert the document
            collection("content").insert_one(data)
            print("Movie Name:", data["movieName"],
                  "is added to the database\n")
        except DuplicateKeyError:
            # Handle the case when a document with the same movieName already exists
            print("Error: Duplicate movieName -",
                  data["movieName"], "Skipping...\n")




def get_popular_movies():
    dotenv.load_dotenv()
    authToken = os.getenv("AUTHORIZATION_TOKEN")
    print("@get_popular_movies")
    databaseOBJ = []

    for i in range(1, 4):
        avarage = (i * 2) - 1
        contentURI = f"https://api.themoviedb.org/3/discover/movie?include_adult=false&include_video=false&page=1&sort_by=popularity.desc&"

        headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {authToken}"
        }
        create_expiry_date = datetime.datetime.now() + datetime.timedelta(days=7)
        response = requests.get(contentURI, headers=headers)
        contentObj = response.json()

        for i in range(len(contentObj["results"])):
            movieTitle = contentObj["results"][i].get("title", "")
            movieId = contentObj["results"][i].get("id", "")
            try:
                release_date_str = contentObj["results"][i].get("release_date")
                if release_date_str:
                    release_date = datetime.datetime.strptime(
                        release_date_str, "%Y-%m-%d").date()
                    if release_date < datetime.date.today():
                        movie_providers = getProvidersWithRetry(movieId)
                        movie_data = get_movie_data(movieTitle)
                        if movie_data is not None:
                            print(movie_data.get("score", ""))
                            print(movieTitle)
                            if not is_valid(movie_data.get("score"), movieTitle):
                                movie_data["score"] = [{
                                    "Source": "TMDB",
                                    "Value": contentObj['results'][i].get('vote_average')
                                }]

                            else:
                                movie_data.setdefault("score", []).append({
                                    "Source": "TMDB",
                                    "Value": contentObj['results'][i].get('vote_average')
                                })
                            if all(is_valid(movie_data[key], movieTitle) for key in ["score", "poster_uri", "description", "runtime"]):
                                databaseOBJ.append({
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
                                    "expiry_date": create_expiry_date,
                                    "movieProvider": movie_providers if movie_providers is not None else None
                                })
                            else:
                                print(f"Error processing movie {movieTitle}: Incomplete data")
                        else:
                            print(f"Error processing movie {movieTitle}: No data returned")
            except ValueError as e:
                # Handle the case when release_date is not a valid date
                print(f"Error processing release_date for movie ", {movieTitle}, {e})
        # Print the formatted data
    for data in databaseOBJ:
        try:
            # Attempt to insert the document
            collection("popular_movies").insert_one(data)
            data["expiry_date"] = None
            collection("content").insert_one(data)
            print("Movie Name:", data["movieName"], " is added to the database\n")
        except DuplicateKeyError:
            # Handle the case when a document with the same movieName already exists
            print("Error: Duplicate movieName -",
                  data["movieName"], "Skipping...\n")
