from bson import ObjectId
from worth2watch.Database.DatabaseModel.contentModel import createCollection as collection


def movie_names():
    movie_names = []
    agragetion = [
        {
            "$group": {
                "_id": "$movieName",
            }
        }
    ]  
    
    response = collection("content").aggregate(agragetion)
    for doc in response:
        movie_dict = {
            "movieName": doc["_id"],
        }
        movie_names.append(movie_dict)

    return movie_names


def add_comments_to_movie(movie_name, reddit_comments, youtube_comments):
    print("@add_comments_to_movie for : ", movie_name, "reddit_comments: ",
          len(reddit_comments), "youtube_comments: ", len(youtube_comments))
    if len(reddit_comments) == 0 and len(youtube_comments) == 0:
        return
    elif len(reddit_comments) == 0:
        update_data = {
            "$set": {
                "Comments": {
                    "youtubeComments": youtube_comments
                }
            }
        }
        collection("content").update_one(
            {'movieName': movie_name}, update_data)
        return
    elif len(youtube_comments) == 0:
        update_data = {
            "$set": {
                "Comments": {
                    "redditComments": reddit_comments
                }
            }
        }
        collection("content").update_one(
            {'movieName': movie_name}, update_data)
        return

    update_data = {
        "$set": {
            "Comments": {
                "redditComments": reddit_comments,
                "youtubeComments": youtube_comments
            }
        }
    }
    collection("content").update_one({'movieName': movie_name}, update_data)


def db_sentiment_analysis(comment, sentiment_analysis, comment_type):
    if comment_type == "reddit":
        query = {"Comments.redditComments.comment": comment}
        collection("content").update_one(query, {"$set": {"Comments.redditComments.$.sentiment": sentiment_analysis}})
    else:
        query = {"Comments.youtubeComments.comment": comment}
        collection("content").update_one(query, {"$set": {"Comments.youtubeComments.$.sentiment": sentiment_analysis}})
    return {"status": "ok"}


def get_comments():
    print("@get_comments")

    # Initialize dictionaries for Reddit and YouTube comments
    reddit_comments = {"type": "reddit", "data": []}
    youtube_comments = {"type": "youtube", "data": []}

    # Retrieve Reddit comments
    response_reddit = collection("content").find(
        {"Comments.redditComments": {"$exists": True}})
    for doc in response_reddit:
        for comment in doc["Comments"]["redditComments"]:
            reddit_comments["data"].append(comment)

    # Retrieve YouTube comments
    response_youtube = collection("content").find(
        {"Comments.youtubeComments": {"$exists": True}})
    for doc in response_youtube:
        for comment in doc["Comments"]["youtubeComments"]:
            youtube_comments["data"].append(comment)

    # Create a list containing the dictionaries for Reddit and YouTube comments
    comments = [reddit_comments, youtube_comments]

    return comments