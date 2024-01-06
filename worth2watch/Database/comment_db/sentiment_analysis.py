from nltk.sentiment import SentimentIntensityAnalyzer

import nltk
nltk.download('vader_lexicon') # Download the lexicon for sentiment analysis if not already downloaded
import time

def analyze_sentiment(comment):
    sentiment_score = 0
    try:
        sia = SentimentIntensityAnalyzer()
        sentiment_score = sia.polarity_scores(comment)["compound"]
        sentiment_score = ((sentiment_score + 1) / 2) * 10
        sentiment_score = round(sentiment_score, 2)
    except Exception as e:
        print("Error in sentiment analysis: ", e)
    print(sentiment_score)
    return sentiment_score

# def calculate_sentiment_ratios(comments):
#     scores_of_comments = [analyze_sentiment(comment) for comment in comments]

#     total_count = len(scores_of_comments)
#     point = (sum(scores_of_comments) / total_count)
#     return point

# sentences_to_analyze = "I love this movie"
# result = analyze_sentiment(sentences_to_analyze)

# print("Ratio of movie:", result)
