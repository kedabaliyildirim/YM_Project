import googleapiclient.discovery
from requests import HTTPError


def get_comment_text(video_id, api_key, maxResults=100):
    api_service_name = "youtube"
    api_version = "v3"
    try:
        youtube = googleapiclient.discovery.build(
            api_service_name, api_version, developerKey=api_key)
        request = youtube.commentThreads().list(
            part="snippet",
            videoId=video_id,
            order="relevance",
            maxResults=maxResults
        )
        response = request.execute()
        comments = []
        for item in response.get('items', []):
            comment_dict = {
                "comment": item.get('snippet', {}).get('topLevelComment', {}).get('snippet', {}).get('textOriginal', '')
            }
            comments.append(comment_dict)
    except HTTPError as e:
        return
    return comments
