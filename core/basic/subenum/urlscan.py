#!/usr/bin/env python3
from sys import exit
import json
import requests


def enumerator(domain):
    domains = []
    try:
        response = requests.get('https://urlscan.io/api/v1/search/', params={'q': f'page.domain:{domain}', 'size': 10000})
        json_response = json.loads(response.text)
        for d in json_response['results']:
            domains.append(d['page']['domain'])

    except requests.ConnectionError:
        pass
    except json.decoder.JSONDecodeError:
        pass
    except KeyboardInterrupt:
        exit('Bye!')
    return set(domains)
