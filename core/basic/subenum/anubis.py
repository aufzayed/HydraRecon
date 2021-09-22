#!/usr/bin/env python3
import requests


def anubis_api(hostname):
    try:
        response = requests.get(f'https://jldc.me/anubis/subdomains/{hostname}')
        domains = [domain for domain in response.json()]
        return set(domains)
    except Exception as e:
        print(f'[!][anubis] Runtime Error: {e}')
        return []
