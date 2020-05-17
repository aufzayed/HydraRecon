#!/usr/bin/env python3
import json
import requests


def enumerator(domain):
    domains = []
    try:
        response = requests.get('https://urlscan.io/api/v1/search/', params={'q': f'page.domain:{domain}', 'size': 10000})
        json_response = json.loads(response.text)
        #total = data['total']
        for d in json_response['results']:
            domains.append(d['page']['domain'])

    except requests.ConnectionError:
        pass
    except json.decoder.JSONDecodeError:
        pass
    return set(domains)
