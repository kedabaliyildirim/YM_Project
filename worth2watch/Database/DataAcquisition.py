import json
import os
import requests
import dotenv
import datetime
from worth2watch.Database.DatabaseModel.contentModel import createCollection as collection
from providerCall import getProviders

def accquireData(pageNo):
    dotenv.load_dotenv()

    contentApiKey = os.getenv("CONTENT_API_KEY")
    authToken = os.getenv("AUTHORIZATION_TOKEN")

    databaseOBJ = []
    genreURI = "https://api.themoviedb.org/3/genre/movie/list?language=en"
    contentURI = f"https://api.themoviedb.org/3/discover/movie?page={pageNo}&sort_by=popularity.desc"
    posterURI = "https://image.tmdb.org/t/p/original{}"
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {authToken}"
    }

    response = requests.get(contentURI, headers=headers)
    genreResponse = requests.get(genreURI, headers=headers)
    contentObj = response.json()
    genreObj = {genre["id"]: genre["name"] for genre in genreResponse.json()["genres"]}
    
    for i in range(len(contentObj["results"])):
        movieTitle = contentObj["results"][i].get("title", "")
        movieId = contentObj["results"][i].get("id", "")
        genreList = [genreObj[genre_id] for genre_id in contentObj["results"][i].get("genre_ids", []) if genre_id in genreObj]

        try:
            release_date_str = contentObj["results"][i].get("release_date")
            if release_date_str:
                release_date = datetime.datetime.strptime(release_date_str, "%Y-%m-%d").date()
                if release_date < datetime.date.today():
                    movie_providers = getProviders(movieId)
                    databaseOBJ.append({
                        "movieName": movieTitle,
                        "movieReleaseDate": release_date_str,
                        "movieGenre": genreList,
                        "imageURL": posterURI.format(contentObj['results'][i].get('backdrop_path')),
                        "movieProvider": movie_providers if movie_providers is not None else None
                    })
        except ValueError as e:
            # Handle the case when release_date is not a valid date
            print(f"Error processing release_date for movie {movieTitle}: {e}")

    # Print the formatted data
    for data in databaseOBJ:
        print("Movie Name: ", data["movieName"] + "is added to database" + "\n")
        collection().insert_one(data)

for i in range(10):
    accquireData(i+1)
