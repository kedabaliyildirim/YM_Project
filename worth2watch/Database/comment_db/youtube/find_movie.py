from googleapiclient.discovery import build
from requests import HTTPError

def storage_checker(movie_names, path="movie_names.txt"):
    try:
        movie_names_storage = open(path, "r")
        movie_names = movie_names_storage.readlines()
        movie_names_storage.close()
    except FileNotFoundError:
        movie_names = []
    return movie_names

def get_youtube_video_id(api_key, query):
    youtube = build('youtube', 'v3', developerKey=api_key)
    storage_status = storage_checker(query)
    if query in storage_status:
        print("Already searched")
        return None
    
    movie_names_storage = open("movie_names.txt", "a")
    try:
        search_response = youtube.search().list(
            q=query,
            part='snippet',
            maxResults=1
        ).execute()
        movie_names_storage.write(f"{query}\n")
        video_id = None
        for search_result in search_response.get('items', []):
            try:
                # Check if the result is a video
                if search_result['id']['kind'] == 'youtube#video':
                    video_id = search_result['id']['videoId']
                    break
            except KeyError as e:
                print(f"Error extracting information: {e}")
    except HTTPError as e:
        return None
    return video_id

# if __name__ == '__main__':
#     search_query = 'Avengers Infinity War'

#     video_id = get_youtube_video_id(api_key, search_query)

#     if video_id:
#         print(f"Video ID: {video_id}")
#     else:
#         print("No video found.")
