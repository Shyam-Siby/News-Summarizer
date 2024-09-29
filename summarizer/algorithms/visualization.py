# summarizer/algorithms/visualization.py
import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
import io
import base64

def plot_sentiment(sentiment):
    """
    Plots the sentiment analysis results.
    :param sentiment: (dict) sentiment classification, polarity, and subjectivity
    :returns: (str) base64 encoded image
    """
    fig, ax = plt.subplots()
    ax.bar(['Polarity', 'Subjectivity'], [sentiment['polarity'], sentiment['subjectivity']])
    ax.set_ylim([-1, 1])
    ax.set_title(f"Sentiment Analysis: {sentiment['classification']}")

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    image_base64 = base64.b64encode(buf.read()).decode('utf-8')
    buf.close()

    return image_base64
