from worth2watch.Database.comment_db.reddit.reddit_api import search_reddit
from worth2watch.Database.comment_db.youtube.yt_trailer_comments import get_youtube_comments
from worth2watch.Database.comment_db.comment_requests import add_comments_to_movie, db_sentiment_analysis, get_comments


def main_agent(movie_name, reddit_status, youtube_status):
    if reddit_status:
        print("@main_agent for : ", movie_name, "reddit_status: ", reddit_status, "youtube_status: ", youtube_status)
        reddit_comments = search_reddit(movie_name, comment_limit=20, search_limit=1, thread_depth=1)
        # print(reddit_comments)
    else:
        reddit_comments = []
        
    if youtube_status:
        youtube_comments = get_youtube_comments(movie_name, 10)
    else:
        youtube_comments = []
    add_comments_to_movie(movie_name= movie_name, reddit_comments=reddit_comments, youtube_comments=youtube_comments)
    return {"status": "ok"}


# def agent_movie_caller(reddit_status, youtube_status):
#     movie_names_list = movie_names()
#     print("@agent_movie_caller")
#     for movie in movie_names_list:
#         main_agent(movie['movieName'], reddit_status=reddit_status,
#                    youtube_status=youtube_status, movie_id=movie['movieId'])
#     return {"status": "ok"}

# def analyse_comments(comment, comment_type):
#     print("@analyse_comments")
#     if comment_type == "reddit":
#         analysis = sentiment_analysis(comment['comment'])
#         db_sentiment_analysis(comment['comment'], analysis, comment_type='reddit')
#     else:
#         analysis = sentiment_analysis(comment['comment'])
#         db_sentiment_analysis(comment['comment'], analysis, comment_type='youtube')
#     return {"status": "ok"}