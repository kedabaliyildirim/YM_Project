import googleapiclient.discovery
import googleapiclient.errors

def get_comment_text(video_id, api_key, maxResults=100):
    api_service_name = "youtube"
    api_version = "v3"

    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey=api_key)

    request = youtube.commentThreads().list(
        part="snippet",
        videoId=video_id,
        maxResults=maxResults
    )
    response = request.execute()

    comments = []
    for item in response.get('items', []):
        comment_text = item.get('snippet', {}).get('topLevelComment', {}).get('snippet', {}).get('textDisplay', '')
        comments.append(comment_text)

    return comments

# # Video ID ve API anahtarını buraya ekleyin
# video_id = "6ZfuNTqbHE8"
# api_key = "AIzaSyCi9sy_YYyqLvfp9kB3DSy7POZyutFhhIg"

# comments = get_comment_text(video_id, api_key)

# for comment in comments:
#     print(comment)
