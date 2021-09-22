#!/usr/bin/env python3
import requests


def certspotter_api(hostname):
    try:
        parameters = {
            'domain': hostname,
            'include_subdomains': True,
            'match_wildcards': True,
            'expand': 'dns_names'
        }
        response = requests.get('https://certspotter.com/api/v1/issuances', params=parameters)
        domains_list = [domain for domain in response.json() for domain in domain['dns_names']]
        return domains_list
    except Exception as e:
        print(f'[!][certspotter] Runtime Error: {e}')
        return []
