#!/usr/bin/env python3
from sys import exit
import base64
import requests


def b64(cursor):
    b64cursor = base64.b64encode(str(f'I{cursor}\n.').encode('utf-8'))
    utf8cursor = b64cursor.decode('utf-8')
    return utf8cursor


def virustotal_api(hostname, apikey=None):
    domains = []
    cursor = 0
    if apikey is not None:
        while True:
            bs64cursor = b64(cursor)
            try:
                response = requests.get(f'https://www.virustotal.com/api/v3/domains/{hostname}/subdomains',
                                        headers={'x-apikey': apikey},
                                        params={'limit': '40', 'cursor': f'{bs64cursor}'})
                json_response = response.json()
                if len(json_response['data']) != 0:
                    for data in json_response['data']:
                        domains.append(data['id'])
                    cursor += 40
                else:
                    break
            except Exception as e:
                print(f'[!][virustotal] Runtime Error: {e}')
    else:
        return domains
    return set(domains)

