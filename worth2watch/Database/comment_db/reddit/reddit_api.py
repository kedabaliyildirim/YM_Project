import requests
import os


def search_reddit(movie_name, search_limit, thread_depth, comment_limit):
    client_id = os.getenv('REDDIT_API_ID')
    client_secret = os.getenv('REDDIT_API_KEY')

    auth_url = 'https://www.reddit.com/api/v1/access_token'
    auth_data = {'grant_type': 'client_credentials'}

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
        comment_url = f'https://oauth.reddit.com/r/{subreddit}/comments/{post_id}.json'
        idParams = {
            'depth': thread_depth,
            'limit': comment_limit,
            'sort': 'top',
        }
        comment_response = requests.get(
            comment_url, headers=headers, params=idParams)

        if comment_response.status_code == 404:
            continue  # Skip if the post is not found

        comments_data = comment_response.json()

        for comment in comments_data[1]['data']['children']:
            try:
                if 'body' in comment['data']:
                    comment_dict = {
                        # "author": comment['data']['author'],
                        "comment": comment['data']['body']
                    }
                    all_comments.append(comment_dict)
            except:
                pass

    return all_comments


# comments_list = search_reddit("Tiny and Ruby: Hell Divin' Women", 1, 1, 40)
# comments_list = search_reddit("Avengers Infinity War", 1, 1, 40)

# print(comments_list)
