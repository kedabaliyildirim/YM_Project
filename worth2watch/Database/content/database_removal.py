import shutil
from worth2watch.Database.DatabaseModel.contentModel import createCollection as collection


def removeData():
    try:
        # Drop the database collection
        collection("content").drop()
        print("Collection dropped successfully.")
    except Exception as e:
        print(f"Error dropping collection: {e}")

    # Specify the folder path you want to delete
    folder_path = './resources'

    try:
        # Use shutil.rmtree to remove the folder and its contents
        shutil.rmtree(folder_path)
        print(f"Folder '{folder_path}' and its contents deleted successfully.")
    except FileNotFoundError:
        print(f"Folder '{folder_path}' not found.")
    except Exception as e:
        print(f"Error deleting folder: {e}")
