from giphypop import translate


def giphy(config, terms):
    """ Return giphy for given terms. """
    terms = ' '.join(terms)
    if terms:
        img = translate(terms, api_key=config['giphy']['api_key'])
    else:
        img = translate('random', api_key=config['giphy']['api_key'])  # hack
    url = img.fixed_height.downsampled.url
    return [url]
