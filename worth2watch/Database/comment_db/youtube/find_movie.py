from googleapiclient.discovery import build

def get_youtube_video_id(api_key, query):
    youtube = build('youtube', 'v3', developerKey=api_key)

    search_response = youtube.search().list(
        q=query,
        part='snippet',
        maxResults=1
    ).execute()

    video_id = None
    for search_result in search_response.get('items', []):
        try:
            # Check if the result is a video
            if search_result['id']['kind'] == 'youtube#video':
                video_id = search_result['id']['videoId']
                break
        except KeyError as e:
            print(f"Error extracting information: {e}")

    return video_id

# if __name__ == '__main__':
#     search_query = 'Avengers Infinity War'

#     video_id = get_youtube_video_id(api_key, search_query)

#     if video_id:
#         print(f"Video ID: {video_id}")
#     else:
#         print("No video found.")
