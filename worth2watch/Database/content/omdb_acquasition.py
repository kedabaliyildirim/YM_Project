import requests
import dotenv
import os

def search_movie(movie_name):
    dotenv.load_dotenv()
    omdb_api_key=os.getenv("OMDB_API_KEY")
    url = "https://www.omdbapi.com/?t={}".format(movie_name)+"&apikey="+omdb_api_key
    print(url)
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        story_info = data["Plot"]
        genres = data["Genre"]
        director = data["Director"]
        runtime=data["Runtime"]
        score=data["imdbRating"]
        return story_info, genres, director, runtime, score
    else:
        return None, None, None, None, None

if __name__ == "__main__":
    movie_name = input("Enter the movie name: ")
    story_info, genres, director, runtime, score = search_movie(movie_name)
    if story_info is not None:
        print("The story plot for the given movie '{}' is: {}".format(movie_name, story_info))
        print("Genres: {}".format(genres))
        print("Director: {}".format(director))
        print("Runtime: {}".format(runtime))
        print("IMDB Rating: {}".format(score))
    else:
        print("Story plot not found for the movie '{}'".format(movie_name))