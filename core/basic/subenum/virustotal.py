#!/usr/bin/env python3
from sys import exit
import base64
import json
import requests


def b64(cursor):
    b64cursor = base64.b64encode(str(f'I{cursor}\n.').encode('utf-8'))
    utf8cursor = b64cursor.decode('utf-8')
    return utf8cursor


def enumerator(domain, apikey=None):
    domains = []
    cursor = 0
    if apikey is not None:
        while True:
            bs64cursor = b64(cursor)
            try:
                response = requests.get(f'https://www.virustotal.com/api/v3/domains/{domain}/subdomains',
                                        headers={'x-apikey': apikey},
                                        params={'limit': '40', 'cursor': f'{bs64cursor}'})
                json_response = json.loads(response.text)
                if len(json_response['data']) != 0:
                    for data in json_response['data']:
                        domains.append(data['id'])
                    cursor += 40
                else:
                    break
            except requests.ConnectionError:
                pass
            except json.decoder.JSONDecodeError:
                pass
            except KeyboardInterrupt:
                exit('Bye!')
    else:
        return domains
    return set(domains)
