import googleapiclient.discovery
import os
def get_comment_text(video_id, api_key, maxResults=100):
    api_service_name = "youtube"
    api_version = "v3"

    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey=api_key)

    request = youtube.commentThreads().list(
        part="snippet",
        videoId=video_id,
        order="relevance",  # Yorumları relevance sırasına göre al
        maxResults=maxResults
    )
    response = request.execute()

    comments = []
    for item in response.get('items', []):
        comment_dict = {
            # "author": item.get('snippet', {}).get('topLevelComment', {}).get('snippet', {}).get('authorDisplayName', ''),
            "comment": item.get('snippet', {}).get('topLevelComment', {}).get('snippet', {}).get('textOriginal', '')
        }
        comments.append(comment_dict)

    return comments

