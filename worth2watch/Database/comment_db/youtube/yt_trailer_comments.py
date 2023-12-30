# from find_movie import get_youtube_video_id
# from get_comments import get_comment_text
from worth2watch.Database.comment_db.youtube.find_movie import get_youtube_video_id
from worth2watch.Database.comment_db.youtube.get_comments import get_comment_text
from dotenv import load_dotenv
import os


def get_youtube_comments(query, max_results=100):
    load_dotenv()
    api = os.getenv('YOUTUBE_API_KEY')
    id = get_youtube_video_id(api, query)
    if id is None:
        return []
    comments = get_comment_text(id, api, max_results)
    return comments


# for comment in get_youtube_comments("Avengers Infinity War"):
#     print(comment)


