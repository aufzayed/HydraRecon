#!/usr/bin/env python3
import requests


def sublist3r_api(hostname):
    try:
        response = requests.get('https://api.sublist3r.com/search.php', params={'domain': hostname})
        subdomains = [d for d in response.json()]
        return set(subdomains)
    except Exception as e:
        print(f'[!][sublit3r] Runtime Error: {e}')
        return []
