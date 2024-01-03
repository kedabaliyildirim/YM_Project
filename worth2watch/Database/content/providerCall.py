import requests
import os
import time
import dotenv

dotenv.load_dotenv()

TMDB_URL = "https://api.themoviedb.org/3/movie/{}/watch/providers"

TMDB_HEADERS = {
    "accept": "application/json",
    "Authorization": f"Bearer {os.getenv('AUTHORIZATION_TOKEN')}"
}


def get_providers_with_retry(movie_id, max_retries=2, delay_seconds=1):
    print(f"Getting providers for movie {movie_id}...")
    provider_response = requests.get(
        TMDB_URL.format(movie_id), headers=TMDB_HEADERS)
    provider_response.raise_for_status()
    provider_obj = provider_response.json()

    if not provider_obj["results"]:
        return None

    movie_providers = {
        region: options["buy"] for region, options in provider_obj["results"].items() if "buy" in options
    }
    return movie_providers
