# from transformers import pipeline
# import time
# def analyze_sentiment_transformers(sentence, model_name="distilbert-base-uncased-finetuned-sst-2-english"):
#     start_date = time.time()
#     sentiment_analyzer = pipeline("sentiment-analysis", model=model_name, revision="714eb0f")
#     result = sentiment_analyzer(sentence)[0]
#     sentiment_type = result['label']
#     end_date = time.time()
#     time_elapsed = end_date - start_date
#     print("Time elapsed for sentiment analysis: {:.2f} seconds".format(time_elapsed))
#     return sentiment_type

# def analyze_sentiments(sentences, model_name="distilbert-base-uncased-finetuned-sst-2-english"):
#     sentiments = [analyze_sentiment_transformers(sentence, model_name) for sentence in sentences]
#     return sentiments

# def calculate_sentiment_ratios(sentiments):
#     positive_count = sentiments.count("POSITIVE")
#     negative_count = sentiments.count("NEGATIVE")
#     total_count = len(sentiments)
    
#     positive_ratio = (positive_count / total_count)
#     negative_ratio = (negative_count / total_count)
    
#     return positive_ratio, negative_ratio, total_count

# def analyze_and_summarize_sentiments(sentences, model_name="distilbert-base-uncased-finetuned-sst-2-english"):
#     sentiments = analyze_sentiments(sentences, model_name)
#     positive_ratio, negative_ratio, total_count = calculate_sentiment_ratios(sentiments)
    
#     result_dict = {
#         "sentiments": sentiments,
#         "positive_ratio": positive_ratio,
#         "negative_ratio": negative_ratio,
#         "total_count": total_count
#     }
    
#     return result_dict


# # # Test etmek için örnek bir kullanım
# # sentences_to_analyze = ["I love this movie", "I don't like this movie", "Meh"]
# # result = analyze_and_summarize_sentiments(sentences_to_analyze)

# # print("Sentiments:", result["sentiments"])
# # # Assuming result is a dictionary with "positive_ratio" and "negative_ratio" keys
# # print("Sentiments:", result["sentiments"])
# # # Assuming result is a dictionary with "positive_ratio" and "negative_ratio" keys

# # print("Positive Ratio: {:.2f}%".format(result["positive_ratio"] * 100))
# # print("Negative Ratio: {:.2f}%".format(result["negative_ratio"] * 100))
# # print("Positive Ratio: {:.2f}%".format(result["positive_ratio"] * 100))
# # print("Negative Ratio: {:.2f}%".format(result["negative_ratio"] * 100))

# # print("Total Count:", result["total_count"])
# # print("Total Count:", result["total_count"])