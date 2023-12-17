from textblob import TextBlob
from translate_tr_eng import translate_text

def sentiment_analysis(text):
    # Translate the text to English
    english_text = translate_text(text)
    
    # Create a TextBlob object
    blob = TextBlob(english_text)

    # Perform sentiment analysis
    sentiment = blob.sentiment.polarity

    # Interpret the sentiment
    if sentiment > 0:
        return "Positive"
    elif sentiment < 0:
        return "Negative"
    else:
        return "Neutral"

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
