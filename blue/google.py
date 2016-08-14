# import googleapi


def search_site(config, terms):
    """ Return seach url for terms against a target site. """
    google_prefix = 'https://www.google.com/search?q='
    site_url = config['google']['site_url']
    if terms:
        reformatted_url = site_url.replace('/', '%2F')
        url = google_prefix + '+'.join(terms) + '+site:' + reformatted_url
    else:
        url = site_url  # if no search terms provided
    return [url]
