#!/usr/bin/env python3
from urllib.parse import urlparse
import requests


def wayback_api(hostname):
    try:
        parameters = \
            {
                'url': f'*.{hostname}/*',
                'output': 'json',
                'collapse': 'urlkey'
            }
        response = requests.get('http://web.archive.org/cdx/search/cdx', params=parameters)
        domains = [urlparse(u[2]).netloc for u in response.json()]
        return set(domains)
    except Exception as e:
        print(f'[!][wayback] Runtime Error: {e}')
        return []

