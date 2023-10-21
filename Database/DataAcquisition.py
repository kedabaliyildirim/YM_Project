import os
import requests
import dotenv
import datetime
from DatabaseModel.contentModel import createCollection as collection

dotenv.load_dotenv()

contentApiKey = os.getenv("CONTENT_API_KEY")
authToken = os.getenv("AUTHORIZATION_TOKEN")

databaseOBJ = []
genreURI = "https://api.themoviedb.org/3/genre/movie/list?language=en"
contentURI = "https://api.themoviedb.org/3/discover/movie?page=150&sort_by=primary_release_date.desc"
headers = {
    "accept": "application/json",
    "Authorization": f"Bearer {authToken}"
}

response = requests.get(contentURI, headers=headers)
genreResponse = requests.get(genreURI, headers=headers)
contentObj = response.json()
genreObj = {genre["id"]: genre["name"]
            for genre in genreResponse.json()["genres"]}
print(contentObj["results"])
for i in range(len(contentObj["results"])):
    title = contentObj["results"][i].get("title", "")
    genreList = [genreObj[genre_id] for genre_id in contentObj["results"][i].get(
        "genre_ids", []) if genre_id in genreObj]

    try:
        release_date_str = contentObj["results"][i].get("release_date")
        if release_date_str:
            release_date = datetime.datetime.strptime(
                release_date_str, "%Y-%m-%d").date()
            print(release_date)
            if release_date < datetime.date.today():
                databaseOBJ.append({
                    'movieName': title,
                    'movieReleaseDate': release_date_str,
                    'movieGenre': genreList
                })
    except ValueError as e:
        # Handle the case when release_date is not a valid date
        print(f"Error processing release_date for movie {title}: {e}")

for data in databaseOBJ:
    print(data)
    collection().insert_one(data)