#!/usr/bin/env python3
import json
import requests


def api(domain):
    """request related urls from urlscan.io"""
    urlscan_urls = []
    try:
        parameters = \
            {
                'q': f'page.domain:{domain}',
                'size': '10000'
            }
        response = requests.get('https://urlscan.io/api/v1/search/', params=parameters)
        json_response = json.loads(response.text)
        for i in json_response['results']:
            urlscan_urls.append(i['page']['url'])

    except requests.ConnectionError:
        pass
    except KeyboardInterrupt:
        exit('Bye!')
    return set(urlscan_urls)