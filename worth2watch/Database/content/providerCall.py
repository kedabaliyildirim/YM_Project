import requests
from requests.adapters import HTTPAdapter
import dotenv
import os
import time

dotenv.load_dotenv()

url = "https://api.themoviedb.org/3/movie/{}/watch/providers"
authToken = os.getenv("AUTHORIZATION_TOKEN")
headers = {
    "accept": "application/json",
    "Authorization": f"Bearer {authToken}"
}


def getProvidersWithRetry(movieId, max_retries=3, delay_seconds=1):
    for attempt in range(max_retries + 1):
        try:
            providerResponse = requests.get(
                url.format(movieId), headers=headers)
            providerResponse.raise_for_status()
            providerOBJ = providerResponse.json()

            if providerOBJ["results"] == {}:
                return None

            movie_providers = {}

            for region, options in providerOBJ["results"].items():
                if "buy" in options:
                    movie_providers[region] = options["buy"]

            return movie_providers

        except (requests.exceptions.ConnectionError, requests.exceptions.HTTPError) as e:
            print(f"Error on attempt {attempt + 1}: {e}")
            if attempt < max_retries:
                if attempt > 0:
                    print(f"Retrying in {delay_seconds} seconds...")
                    time.sleep(delay_seconds)
            else:
                print(f"Max retries reached. Giving up.")
                return None
        except Exception as e:
            print(f"Unexpected error: {e}")
            return None


# Usage
# result = getProvidersWithRetry(5375264)
# print(result)
