#!/usr/bin/env python3
import requests
import json
from concurrent.futures import ThreadPoolExecutor

URLs = set()


def get_apis():
    cdx_apis = []
    index_collection = requests.get('https://index.commoncrawl.org/collinfo.json')
    apis = json.loads(index_collection.text)
    for api in apis:
        cdx_apis.append(api['cdx-api'])
    return cdx_apis


def requester(api, domain):
    parameters = \
        {
            'url': f'*.{domain}/*',
            'output': 'json'
        }
    res = requests.get(api, params=parameters)
    if res.status_code == 200:
        results = [json.loads(result) for result in res.text.splitlines()]
        for result in results:
            URLs.add(result['url'])


def api(domain):
    api_list = get_apis()
    with ThreadPoolExecutor(max_workers=len(api_list)) as exec:
        for link in api_list:
            exec.submit(requester, link, domain)
