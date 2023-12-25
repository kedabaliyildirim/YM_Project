from worth2watch.Database.DatabaseModel.contentModel import createCollection as collection
from bson import json_util
from bson.objectid import ObjectId
from worth2watch.Database.content.DataAcquisition import get_popular_movies
from worth2watch.Database.DatabaseInitialization import initDatabase
import json
from pymongo import DESCENDING, ASCENDING
import pymongo
import datetime

def get_all_movies():
    documents = collection("content").find({})
    json_docs = []

    for doc in documents:
        json_docs.append(json.loads(
            json_util.dumps(doc, default=json_util.default)))
    return json_docs


def getPaginatedData(page, page_size, sort_by, sort_order):
    json_docs = []
    order = -1 if sort_order == -1 else 1

    if sort_by == 'movieName' or sort_by == 'movieReleaseDate':
        if sort_by == 'movieReleaseDate':
            order = 1 if sort_order == -1 else -1
            coll = collection("content").find({}).sort([(sort_by, order)]).skip(
                (page - 1) * page_size).limit(page_size)
        else:
            coll = collection("content").find({})

        for doc in coll:
            json_docs.append(json_util.dumps(doc, default=json_util.default))

    elif sort_by == 'imdbRating':
        aggregation_pipeline = [
            {
                '$unwind': '$movieScore'
            },
            {
                '$addFields': {
                    'imdbRating': {
                        '$cond': {
                            'if': {
                                '$eq': [
                                    '$movieScore.Source', 'Internet Movie Database'
                                ]
                            },
                            'then': '$movieScore.Value',
                            'else': None
                        }
                    }
                }
            },
            {
                '$sort': {
                    'imdbRating': order
                }
            },
            {
                '$skip': (page - 1) * page_size
            },
            {
                '$limit': page_size
            }
        ]
        coll = collection("content").aggregate(aggregation_pipeline)
        for doc in coll:
            json_docs.append(json_util.dumps(doc, default=json_util.default))
    elif sort_by == 'tmdbRating':
        aggregation_pipeline = [
            {
                '$unwind': '$movieScore'
            },
            {
                '$addFields': {
                    'tmdbRating': {
                        '$cond': {
                            'if': {
                                '$eq': [
                                    '$movieScore.Source', 'TMDB'
                                ]
                            },
                            'then': '$movieScore.Value',
                            'else': None
                        }
                    }
                }
            },
            {
                '$sort': {
                    'tmdbRating': order
                }
            },
            {
                '$skip': (page - 1) * page_size
            },
            {
                '$limit': page_size
            }
        ]
        coll = collection("content").aggregate(aggregation_pipeline)
        for doc in coll:
            json_docs.append(json_util.dumps(doc, default=json_util.default))
    return json_docs


def totalPages(page_size):
    total = collection("content").count_documents({})
    return total // page_size


def getRequestedMovie(movieId):
    objInstance = ObjectId(movieId)
    document = collection("content").find_one({"_id": objInstance})
    json_document = json_util.dumps(document)
    return json_document


def getSearchedMovie(searchedMovie):
    # Split the input string into individual words
    pipeline = [
        {
            '$search': {
                'index': 'autoName',
                'compound': {
                    'should': [
                        {
                            'autocomplete': {
                                'query': searchedMovie,
                                'path': 'movieName'
                            }
                        },
                    ],
                    'minimumShouldMatch': 1
                }
            }
        },
        {
            '$limit': 5
        },
    ]

    # Execute the aggregate query using the provided MongoDB connection
    coll = collection("content").aggregate(pipeline)
    # Convert the result documents to JSON
    json_documents = [json_util.dumps(doc) for doc in coll]
    return json_documents


def acquire_top_ten():
    print("@acquire_top_ten")
    if collection("popular_movies").count_documents({}) > 0:
        print("database is not empty")
        today = datetime.datetime.now()
        dbExpiryDate = collection("popular_movies").find_one(
            {"expiry_date": {"$exists": True}})
        if dbExpiryDate is not None:
            if dbExpiryDate["expiry_date"] > today:
                databaseOBJ = collection("popular_movies").find({}).limit(10)
                json_documents = [json_util.dumps(doc) for doc in databaseOBJ]
                return json_documents
            else:
                print("Popular movies are not up to date")
                collection("popular_movies").drop()
                print("Popular movies are dropped")

                get_popular_movies()
                databaseOBJ = collection("popular_movies").find({}).limit(10)
                json_documents = [json_util.dumps(doc) for doc in databaseOBJ]
                return json_documents
    else:
        print("Popular movies are not in the database")
        get_popular_movies()
        databaseOBJ = collection("popular_movies").find({}).limit(10)
        json_documents = [json_util.dumps(doc) for doc in databaseOBJ]
        return json_documents
