import nltk
from nltk.sentiment import SentimentIntensityAnalyzer

# NLTK'nin sentiment analizi için gereken kaynakları indirme
nltk.download('vader_lexicon')

def sentiment_analysis(text):
    # SentimentIntensityAnalyzer sınıfını oluştur
    sia = SentimentIntensityAnalyzer()

    # Metni analiz et ve sentiment skorlarını al
    sentiment_scores = sia.polarity_scores(text)

    # Sentiment skorlarını ekrana yazdır
    print("Sentiment Scores:", sentiment_scores)

    
    # if sentiment_scores['compound'] >= 0.05:
    #     sentiment = 'Positive'
    # elif sentiment_scores['compound'] <= -0.05:
    #     sentiment = 'Negative'
    # else:
    #     sentiment = 'Neutral'

    return sentiment_scores['compound']/0.6369

# # Duygu analizi yapılacak metni girin
# text_to_analyze = "I don't like it"

# # Duygu analizini yap
# result = sentiment_analysis(text_to_analyze)

# # Sonucu ekrana yazdır
# print("Sentiment:", result)
