from bson import ObjectId
from worth2watch.Database.DatabaseModel.contentModel import createCollection as collection

def movie_names():
    movie_names = []
    response = collection("content").find({})
    for doc in response:
        movie_dict = {
            "movieName": doc["movieName"],
            "movieId": str(doc["_id"])
        }
        movie_names.append(movie_dict)

    return movie_names


def add_comments_to_movie(movie_name, reddit_comments, youtube_comments):
    print("@add_comments_to_movie for : ", movie_name, "reddit_comments: ", len(reddit_comments), "youtube_comments: ", len(youtube_comments))
    update_data = {
        "$set": {
            "Comments": {
                "redditComments": reddit_comments,
                "youtubeComments": youtube_comments
            }
        }
    }
    collection("content").update_one({'movieName' : movie_name}, update_data)
