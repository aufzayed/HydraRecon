#!/usr/bin/env python3
import json
import requests
import base64


def wayback_machine(domain):
    """request web site urls from web archive"""
    wayback_urls = []
    try:
        parameters = \
            {
                'url': f'{domain}/*',
                'output': 'json',
                'collapse': 'urlkey'
            }
        response = requests.get('http://web.archive.org/cdx/search/cdx', params=parameters)
        json_response = json.loads(response.text)
        for url in json_response:
            try:
                wayback_urls.append(url[2])
            except IndexError:
                pass
    except requests.ConnectionError:
        pass
    except requests.exceptions.ChunkedEncodingError:
        pass
    except json.decoder.JSONDecodeError:
        pass
    return set(wayback_urls)


def common_crawl(domain):
    """request urls from common crawl"""
    commoncrawl_urls = []
    try:
        #  fetch current index collections
        index_collection = requests.get('https://index.commoncrawl.org/collinfo.json')
        if index_collection.status_code == 200:
            json_index = json.loads(index_collection.text)
            try:
                for api in json_index:
                    parameters = \
                        {
                            'url': f'{domain}/*',
                            'output': 'json'
                        }

                    response = requests.get(api['cdx-api'], params=parameters)
                    if response.status_code == 200:
                        results = [json.loads(result) for result in response.text.splitlines()]
                        for result in results:
                            commoncrawl_urls.append(result['url'])
            except requests.exceptions.ChunkedEncodingError:
                pass
            except requests.ConnectionError:
                pass
        else:
            pass
    except requests.ConnectionError:
        pass
    return set(commoncrawl_urls)


def url_scan(domain):
    """request related urls from urlscan.io"""
    urlscan_urls = []
    try:
        parameters = \
            {
                'q': f'page.domain:{domain}',
                'size': '10000'
            }
        response = requests.get('https://urlscan.io/api/v1/search/', params=parameters)
        json_response = json.loads(response.text)
        for i in json_response['results']:
            urlscan_urls.append(i['page']['url'])

    except requests.ConnectionError:
        pass
    return set(urlscan_urls)


def b64(cursor):
    b64cursor = base64.b64encode(str(f'I{cursor}\n.').encode('utf-8'))
    utf8cursor = b64cursor.decode('utf-8')
    return utf8cursor


def virus_total(domain, apikey=None):
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
    else:
        pass
    return set(virustotal_urls)

