from nltk.sentiment import SentimentIntensityAnalyzer

def analyze_sentiment(text):
    sia = SentimentIntensityAnalyzer()
    sentiment_score = sia.polarity_scores(text)["compound"]
    sentiment_score = ((sentiment_score + 1) / 2 )*10
    return sentiment_score

def calculate_sentiment_ratios(comments):
    scores_of_comments = [analyze_sentiment(comment) for comment in comments]

    total_count = len(scores_of_comments)
    point = (sum(scores_of_comments) / total_count)
    return "{:.2f}".format(point)

# sentences_to_analyze = ["I love this movie", "I don't like this movie", "Meh"]
# result = calculate_sentiment_ratios(sentences_to_analyze)

# print("Ratio of movie:", result)
