import requests
import os
def search_reddit(movie_name, search_limit, thread_depth, comment_limit):
    client_id = os.getenv('REDDIT_CLIENT_ID')
    client_secret = os.getenv('REDDIT_CLIENT_SECRET')

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
        #  'hot', 'top', 'new', 'comments'.
        'sort': 'relevance',
    }

    headers = {'Authorization': f'bearer {access_token}', 'User-Agent': 'your_app_name'}
    search_response = requests.get(search_url, headers=headers, params=params)
    post_ids = [child['data']['id']  
                for child in search_response.json()['data']['children']]

    for post_id in post_ids:
        comment_url = f'https://oauth.reddit.com/r/{subreddit}/comments/{post_id}'
        idParams = {
            'depth': thread_depth,
            'limit': comment_limit,
            'sort': 'top',
        }
        comment_response = requests.get(
            comment_url, headers=headers, params=idParams)
        return comment_response.json()
