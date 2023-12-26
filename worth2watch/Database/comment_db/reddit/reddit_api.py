import requests
import json
import os


def search_reddit(movie_name, search_limit, thread_depth, comment_limit):
    client_id = os.getenv('REDDIT_API_ID')
    client_secret = os.getenv('REDDIT_API_KEY')

    auth_url = 'https://www.reddit.com/api/v1/access_token'
    auth_data = {
        'grant_type': 'client_credentials',
    }

    auth_response = requests.post(
        auth_url,
        auth=(client_id, client_secret),
        data=auth_data,
        headers={'User-Agent': 'worth2watch'}
    )
    auth_data = auth_response.json()
    access_token = auth_data['access_token']

    subreddit = 'movies'
    search_query = movie_name
    limit = search_limit

    search_url = f'https://oauth.reddit.com/r/{subreddit}/search'
    params = {
        'q': search_query,
        'limit': limit,
        'sort': 'relevance',
    }

    headers = {'Authorization': f'bearer {
        access_token}', 'User-Agent': 'worth2watch'}
    search_response = requests.get(search_url, headers=headers, params=params)
    post_ids = [child['data']['id']
                for child in search_response.json()['data']['children']]

    all_comments = []

    for post_id in post_ids:
        comment_url = f'https://oauth.reddit.com/r/{
            subreddit}/comments/{post_id}.json'
        idParams = {
            'depth': thread_depth,
            'limit': comment_limit,
            'sort': 'top',
        }
        comment_response = requests.get(
            comment_url, headers=headers, params=idParams)
        comments_data = comment_response.json()

        # Access and print the body of each comment
        for comment in comments_data[1]['data']['children']:
            if 'body' in comment['data']:
                comment_dict = {
                    "author": comment['data']['author'],
                    "comment": comment['data']['body']
                }
                all_comments.append(comment_dict)

    # Convert the list of dictionaries to a JSON string
    json_comments = json.dumps(all_comments, indent=2)

    # Optionally, you can save the JSON string to a file
    with open('comments.json', 'w') as json_file:
        json_file.write(json_comments)

    return all_comments


# comments_list = search_reddit("Avengers endgame", 1, 1, 3)
# print(comments_list)