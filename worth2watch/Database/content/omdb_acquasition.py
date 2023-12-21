import requests
import dotenv
import os


def get_movie_data(movie_name):
    dotenv.load_dotenv()
    omdb_api_key = os.getenv("OMDB_API_KEY")
    url = "https://www.omdbapi.com/?t={}".format(
        movie_name)+"&apikey="+omdb_api_key
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data["Response"] == "False":
            return None
        description = data["Plot"]
        writer = data["Writer"]
        actors = data["Actors"]
        genres = data["Genre"]
        director = data["Director"]
        runtime = data["Runtime"]
        poster_uri = data["Poster"]
        score = data["Ratings"]
        database_object = {
            "movie_name": movie_name,
            "description": description,
            "writer": writer,
            "actors": actors,
            "genres": genres,
            "runtime": runtime,
            "poster_uri": poster_uri,
            "score": score,
            "director": director,
        }
        return database_object
    else:
        return None


