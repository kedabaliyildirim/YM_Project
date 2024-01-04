from nltk.sentiment import SentimentIntensityAnalyzer
import time
def analyze_sentiment(text):
    start_date = time.time()
    sia = SentimentIntensityAnalyzer()
    sentiment_score = sia.polarity_scores(text)["compound"]
    sentiment_score = (sentiment_score + 1)/2 
    end_date = time.time()
    time_elapsed = end_date - start_date
    print("Time elapsed for sentiment analysis: {:.2f} seconds".format(time_elapsed)) 
    return sentiment_score

def calculate_sentiment_ratios(comments):
    scores_of_comments = [analyze_sentiment(comment) for comment in comments]

    total_count = len(scores_of_comments)
    ratio = sum(scores_of_comments)/total_count
    return ratio

sentences_to_analyze = ["I love this movie", "I don't like this movie", "Meh"]
result = calculate_sentiment_ratios(sentences_to_analyze)

print("Ratio of movie", result)