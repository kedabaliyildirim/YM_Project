import os
import praw


def search_reddit(movie_name, search_limit, thread_depth, comment_limit):
    reddit = praw.Reddit(
        client_id=os.getenv('REDDIT_API_ID'),
        client_secret=os.getenv('REDDIT_API_KEY'),
        user_agent='worth2watch',
    )

    subreddit = reddit.subreddit('movies')
    search_query = movie_name
    limit = search_limit

    search_results = subreddit.search(
        query=search_query,
        sort='relevance',
        time_filter='all',
        limit=limit,
    )

    all_comments = []

    for submission in search_results:
        # Replace 'limit' with the desired number
        submission.comments.replace_more(limit=0)
        comments = submission.comments.list()

        for comment in comments:
            try:
                if comment.body:
                    # VAKKAS RUN SENTIMENT ANALYSIS HERE
                    # LIKE THIS: sentiment = sentiment_analysis(comment.body)
                    comment_dict = {
                        "comment": comment.body,
                        # "sentiment": sentiment,
                    }
                    all_comments.append(comment_dict)
            except Exception as e:
                print(f"Error processing comment: {e}")

    return all_comments


# comments_list = search_reddit("Tiny and Ruby: Hell Divin' Women", 1, 1, 40)
# print(comments_list)