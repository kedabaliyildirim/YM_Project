import requests
import dotenv
import os
dotenv.load_dotenv()
url = "https://api.themoviedb.org/3/movie/{}/watch/providers"
authToken = os.getenv("AUTHORIZATION_TOKEN")
headers = {
    "accept": "application/json",
    "Authorization": f"Bearer {authToken}"
}

def getProviders(movieId):
    providerResponse = requests.get(url.format(movieId), headers=headers)
    providerOBJ = providerResponse.json()
    if (providerOBJ["results"] == {}):
        return None
    movie_providers = {}

    for region, options in providerOBJ["results"].items():
        if "buy" in options:
            movie_providers[region] = options["buy"]
    
    return  movie_providers

getProviders(575264)