#!/usr/bin/env python3
import json
import requests


def enumerator(domain):
    domains = []
    parameters = \
        {
            'fields': 'subjectCNReversed',
            'domain': domain,
            'includeExpired': 'true',
            'exactMatch': 'false',
            'limit': 5000
        }
    try:
        response = requests.get('https://ctsearch.entrust.com/api/v1/certificates', params=parameters)
        json_data = json.loads(response.text)
        for result in json_data:
            domains.append(result['subjectCNReversed'][::-1])
        return set(domains)
    except requests.ConnectionError:
        pass
    except json.decoder.JSONDecodeError:
        return []
