#!/usr/bin/env python3
import requests


def threadcrowd_api(hostname):
    try:
        response = requests.get('https://www.threatcrowd.org/searchApi/v2/domain/report/', params={'domain': hostname})
        domains = [domain for domain in response.json()['subdomains']]
        return set(domains)
    except Exception as e:
        print(f'[!][threadcrowd] Runtime Error: {e}')
        return []
