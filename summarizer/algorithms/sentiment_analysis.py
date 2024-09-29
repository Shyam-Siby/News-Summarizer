from textblob import TextBlob

def analyze_sentiment(text):
    """
    Analyzes the sentiment of the given text.
    :param text: (str) text to analyze
    :returns: (dict) sentiment classification and subjectivity
    """
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity
    subjectivity = blob.sentiment.subjectivity

    if polarity > 0:
        sentiment_classification = 'Positive'
    elif polarity < 0:
        sentiment_classification = 'Negative'
    else:
        sentiment_classification = 'Neutral'

    sentiment = {
        'classification': sentiment_classification,
        'polarity': polarity,
        'subjectivity': subjectivity
    }
    return sentiment
