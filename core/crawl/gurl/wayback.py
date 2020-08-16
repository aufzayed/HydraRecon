#!/usr/bin/env python3
import requests
import json


def api(domain):
    """request web site urls from web archive"""
    wayback_urls = []
    try:
        parameters = \
            {
                'url': f'*.{domain}/*',
                'output': 'json',
                'collapse': 'urlkey'
            }
        response = requests.get('http://web.archive.org/cdx/search/cdx', params=parameters)
        json_response = json.loads(response.text)
        for url in json_response:
            try:
                wayback_urls.append(url[2])
            except IndexError:
                pass
    except requests.ConnectionError:
        pass
    except requests.exceptions.ChunkedEncodingError:
        pass
    except json.decoder.JSONDecodeError:
        pass
    except KeyboardInterrupt:
        exit('Bye!')
    return set(wayback_urls)