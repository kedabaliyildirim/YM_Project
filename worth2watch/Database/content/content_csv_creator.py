import csv
import os
import shutil
import time
import requests
from worth2watch.Database.content.DatabaseRequests import get_all_movies
import json
from bson import json_util
import re

def sanitize_filename(filename):
    # Replace invalid characters with underscores
    return re.sub(r'[\\/:"*?<>|]', '_', filename)

def save_image_from_url(url, local_path):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an HTTPError for bad responses
        with open(local_path, 'wb') as file:
            file.write(response.content)
        print(f"Image saved to {local_path}")
    except requests.exceptions.RequestException as e:
        print(f"Error downloading image: {e}")
        # Log the full exception traceback for better debugging
        import traceback
        traceback.print_exc()


def save_movie_data_to_csv(movie_data_list, image_folder='', output_folder='./resources/', country_code='US'):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    if not os.path.exists(image_folder):
        os.makedirs(image_folder)
    csv_file_path = os.path.join(output_folder, 'movies_metadata.csv')

    with open(csv_file_path, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ["image", "Title", "Description", "Writer", "Actirs",
                      "Genres", "Director", "Runtime", "Release Date", "Provider", "Rating"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for movie_data in movie_data_list:
            movie_name = movie_data.get("movieName")
            image_url = movie_data.get("imageURL")

            # Check if movie_name and image_url are not None before proceeding
            if movie_name is not None and image_url is not None:
                # Sanitize movie name for creating a valid file path
                sanitized_movie_name = sanitize_filename(movie_name)

                # Save image locally to .\\resources\\image_resources
                image_filename = f"{sanitized_movie_name}_poster.jpg"
                image_path = os.path.join(image_folder, image_filename)
                if not os.path.exists(image_path):
                    save_image_from_url(image_url, image_path)

                # Update the image URL to point to the local path
                movie_data["imageURL"] = image_path

                # Extract US providers
                if movie_data.get("movieProvider") is not None and movie_data.get("movieProvider", {}).get(country_code) is not None:
                    us_providers = movie_data.get(
                        "movieProvider", {}).get(country_code, [])

                    # Extract provider names
                    provider_names = [provider.get(
                        'provider_name', '') for provider in us_providers]
                else:
                    # If there are no providers, set provider_names to None
                    provider_names = ["no providers found"]

                writer.writerow({
                    "image": image_path,
                    "Title": movie_name,
                    "Description": movie_data.get("movieDescription", ""),
                    "Writer": movie_data.get("movieWriter", ""),
                    "Actirs": movie_data.get("movieActors", ""),
                    "Genres": movie_data.get("movieGenres", ""),
                    "Director": movie_data.get("movieDirector", ""),
                    "Runtime": movie_data.get("movieRuntime", ""),
                    "Release Date": movie_data.get("movieReleaseDate", ""),
                    "Provider": ', '.join(provider_names),
                    "Rating": json.dumps(movie_data.get("movieScore", {"Source": "", "Value": ""}))
                })

    print(f"CSV file and images saved to {output_folder}")


def create_csv_from_database():
    # Specify the folder path you want to delete
    folder_path = './resources'

    try:
        # Use shutil.rmtree to remove the folder and its contents
        shutil.rmtree(folder_path)
        print(f"Folder '{folder_path}' and its contents deleted successfully.")
    except FileNotFoundError:
        print(f"Folder '{folder_path}' not found.")
    except PermissionError:
        # If there's a permission error, wait for a few seconds and try again
        print("Permission error. Retrying in 5 seconds...")
        time.sleep(5)
        try:
            shutil.rmtree(folder_path)
            print(
                f"Folder '{folder_path}' and its contents deleted successfully.")
        except Exception as e:
            print(f"Error deleting folder: {e}")
    except Exception as e:
        print(f"Error deleting folder: {e}")

    # Move the following lines inside the try block
    movies = get_all_movies()
    output_folder = os.path.join(".", "resources", "image_resources")
    save_movie_data_to_csv(movies, output_folder)
