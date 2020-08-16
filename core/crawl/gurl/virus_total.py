#!/usr/bin/env python3
import base64
import json
import requests


def b64(cursor):
    b64cursor = base64.b64encode(str(f'I{cursor}\n.').encode('utf-8'))
    utf8cursor = b64cursor.decode('utf-8')
    return utf8cursor


def api(domain, apikey=None):
    """ request related urls form virus total"""
    virustotal_urls = []
    cursor = 0
    if apikey is not None:
        while True:
            try:
                parameters = \
                    {
                        'limit': '40',
                        'cursor': f'{b64(cursor)}'
                    }
                response = requests.get(f'https://www.virustotal.com/api/v3/domains/{domain}/urls',
                                        headers={'x-apikey': apikey},
                                        params=parameters)
                json_response = json.loads(response.text)
                if len(json_response['data']) != 0:
                    for data in json_response['data']:
                        virustotal_urls.append(data['attributes']['url'])
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
        pass
    return set(virustotal_urls)