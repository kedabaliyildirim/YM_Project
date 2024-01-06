import os
import praw
import logging

def search_reddit(movie_name, search_limit, thread_depth, comment_limit):
    reddit = praw.Reddit(
        client_id=os.getenv('REDDIT_API_ID'),
        client_secret=os.getenv('REDDIT_API_KEY'),
        user_agent='worth2watch',
        ratelimit_seconds=100,
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
        submission.comments.replace_more(limit=20)
        comments = submission.comments.list()

        for comment in comments:
            try:
                if comment.body and len(all_comments) < comment_limit:
                    # VAKKAS RUN SENTIMENT ANALYSIS HERE
                    # LIKE THIS: sentiment = sentiment_analysis(comment.body)
                    comment_dict = {
                        "comment": comment.body,
                        # "sentiment": sentiment,
                    }
                    all_comments.append(comment_dict)
                    
                    if len(all_comments) >= comment_limit:
                        break  # Break the loop if the comment limit is reached
            except Exception as e:
                print(f"Error processing comment: {e}")

    return all_comments