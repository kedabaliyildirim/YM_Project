from worth2watch.Database.DatabaseModel.contentModel import createCollection as collection
from bson import json_util


def getData():
    documents = collection().find()

    # Create a list to store JSON representations of documents
    json_documents = []

    # Iterate through documents and convert each to JSON
    for document in documents:
        json_document = json_util.dumps(document)
        json_documents.append(json_document)
    return json_documents