from textblob import TextBlob


def mood(config, terms):
    """ Return sentiment of a given phrase. """
    blob = TextBlob(' '.join(terms))
    if blob:
        score = blob.sentiment.polarity
    else:
        score = 0
    return [str(score) + ' on a scale of -1 to 1']
