from bson import ObjectId
import random
from worth2watch import agent_main
from worth2watch.Database.DatabaseModel.contentModel import createCollection as collection
from worth2watch.Database.comment_db.sentiment_analysis import analyze_and_summarize_sentiments


def movie_names():
    movie_names = []
    agragetion = [
        {
            "$group": {
                "_id": "$movieName",
            }
        },
        
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
    try:
        doc = collection("content").find_one({"movieName": movie_name})
        try:
            reddit_comments = doc["Comments"]["redditComments"] + \
                reddit_comments
        except:
            pass
        try:
            youtube_comments = doc["Comments"]["youtubeComments"] + \
                youtube_comments
        except:
            pass
        query = {"movieName": movie_name}
        collection("content").update_one(
            query, {"$set": {"Comments.redditComments": reddit_comments, "Comments.youtubeComments": youtube_comments}})
        return {"status": "ok"}

    except Exception as e:
        print(e)
        return {"status": "error"}


def db_sentiment_analysis(is_reddit=False, is_youtube=False, movieName=None):
    if is_reddit:
        aggragete_pipeline = [
            {
                "$match": {
                    "movieName": movieName
                }
            },
            {
                "$group": {
                    "_id": "$Comments.redditComments.comment",
                }
            }
           
        ]
        docs = collection("content").aggregate(aggragete_pipeline)
        for doc in docs:
            for comment in doc["_id"]:
                print(comment)
                get_random_no =  random.randint(1, 10)
                collection("content").find_one_and_update({"Comments.redditComments.comment": comment}, {
                    "$set": {"Comments.redditComments.$.sentiment": get_random_no}})


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


def print_empty_comments():
    empty_comments = collection('content').find(
        {"Comments": {"$exists": False}})
    empty_names = []
    for col in empty_comments:
        empty_names.append(col['movieName'])
    return empty_names


def empty_youtube_comments():
    aggregate = [
        {
            "$match": {
                "Comments.youtubeComments": []
            }
        },
        {
            "$group": {
                "_id": "$movieName"
            }
        }
    ]
    movie_names = []
    coll = collection("content").aggregate(aggregate)
    for doc in coll:
        movie_names.append(doc["_id"])

    return movie_names


def reddit_comments():
    agragetion_pipeline = [
        {
            '$project': {
                '_id': 0,
                'movieName': 1,
                'Comments': '$Comments.redditComments.comment'
            }
        }
    ]
    coll = collection("content").aggregate(agragetion_pipeline)
    for doc in coll:
        for comment in doc["Comments"]:
            print(comment)
            # TODO: connect to sentiment analysis and add sentiment to comment object
            analysed_comment = {
                "comment": comment,
                "sentiment": "VAL"
            }
            collection("test_sentiment").find_one_and_update({"Comments.redditComments.comment": comment}, {
                "$set": {"Comments.redditComments.$": analysed_comment}})
