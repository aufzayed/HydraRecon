#!/usr/bin/env python3
import requests


def alienvault_api(hostname):
    try:
        response = requests.get(f'https://otx.alienvault.com/api/v1/indicators/domain/{hostname}/passive_dns')
        domains = [d['hostname'] for d in response.json()['passive_dns']]
        return set(domains)
    except Exception as e:
        print(f'[!][alienvault] Runtime Error: {e}')
        return []
