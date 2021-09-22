#!/usr/bin/env python3
import requests


def urlscan_api(hostname):
    try:
        response = requests.get('https://urlscan.io/api/v1/search/', params={'q': f'page.domain:{hostname}', 'size': 10000})
        domains = [d['page']['domain'] for d in response.json()['results']]
        return set(domains)
    except Exception as e:
        print(f'[!][urlscan] Runtime Error: {e}')
        return []
