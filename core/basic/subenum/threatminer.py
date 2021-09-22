#!/usr/bin/env python3
import requests


def threatminer_api(hostname):
    try:
        response = requests.get('https://api.threatminer.org/v2/domain.php', params={'q': hostname, 'rt': 5})
        domains = [d for d in response.json()['results']]
        return set(domains)
    except Exception as e:
        print(f'[!][threatminer] Runtime Error: {e}')
        return []
