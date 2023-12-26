from worth2watch.Database.comment_db.reddit.reddit_api import search_reddit
from worth2watch.Database.comment_db.youtube.yt_trailer_comments import get_youtube_comments
from worth2watch.Database.comment_db.comment_requests import add_comments_to_movie, movie_names
def main_agent(movie_name, reddit_status, youtube_status, movie_id):
    if reddit_status:
        reddit_comments = search_reddit(movie_name, comment_limit=50, search_limit=1, thread_depth=1)
    else:
        reddit_comments = []
    if youtube_status:
        youtube_comments = get_youtube_comments(movie_name, 100)
    else:
        youtube_comments = []
    add_comments_to_movie(movie_id=movie_id, reddit_comments=reddit_comments, youtube_comments=youtube_comments)
    return {"status": "ok"}
# print(main_agent("Avengers Infinity War", True, True))


def agent_movie_caller(reddit_status, youtube_status):
    movie_names_list = movie_names()
    for movie in movie_names_list:
        main_agent(movie['movieName'], reddit_status= reddit_status, youtube_status= youtube_status, movie_id= movie['movieId'])