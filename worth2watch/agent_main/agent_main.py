from worth2watch.Database.comment_db.reddit.reddit_api import search_reddit
from worth2watch.Database.comment_db.youtube.yt_trailer_comments import get_youtube_comments
from worth2watch.Database.comment_db.comment_requests import movie_names
def main_agent(movie_name, reddit_status, youtube_status):
    if reddit_status:
        reddit_comments = search_reddit(movie_name, comment_limit=50, search_limit=1, thread_depth=1)
    if youtube_status:
        youtube_comments = get_youtube_comments(movie_name, 100)
    return reddit_comments, youtube_comments
# print(main_agent("Avengers Infinity War", True, True))
def agent_movie_caller(is_reddit, is_youtube):
    movie_names_list = movie_names()
    for movie in movie_names_list:
        main_agent(movie['movieName'], reddit_status= is_reddit, youtube_status= is_youtube)