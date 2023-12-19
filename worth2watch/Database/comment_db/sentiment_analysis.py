from textblob import TextBlob

def sentiment_analysis(text):
    # Translate the text to English
    
    
    # Create a TextBlob object
    blob = TextBlob(text)

    # Perform sentiment analysis
    sentiment = blob.sentiment.polarity

    return sentiment

    # # Interpret the sentiment
    # if sentiment > 0:
    #     return "Positive"
    # elif sentiment < 0:
    #     return "Negative"
    # else:
    #     return "Neutral"

def main():
    # Take text input from the user
    text = input("Enter the text for sentiment analysis: ")

    # Perform sentiment analysis
    result = sentiment_analysis(text)

    # Print the result to the screen
    print(f"Sentiment of the text: {result}")

# Call the main function
if __name__ == "__main__":
    main()
