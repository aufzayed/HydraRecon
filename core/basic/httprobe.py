#!/usr/bin/env/ python3
import json
import requests
from sys import exit
from urllib.parse import urlparse
from core.basic.helpers import sanitizer, relative_to_absolute


USER_AGENT = 'Mozilla/5.0 (Windows NT 6.3; Win64; x64; rv:76.0) Gecko/20100101 Firefox/76.0'
session_json = []


def probe(domain, path_to_save, timeout=1, user_agent=USER_AGENT):
    response = []
    try:
        http_response = requests.get(f'http://{domain}/', timeout=timeout, headers={'User-Agent': user_agent})
        sanitized_url = sanitizer(f'http://{domain}/')
        url = urlparse(http_response.url)
        html_session = {
                'file_name': sanitized_url,
                'url': f'http://{domain}',
                'domain': f'{domain}',
                'status_code': http_response.status_code,
                'headers': dict(http_response.headers),
            }
        session_json.append(html_session)

        print(f'[#] {domain} -> {url.scheme}://{url.hostname} :: {http_response.status_code}')
        with open(f'{path_to_save}/hydra_report/response_body/{sanitized_url}.html', 'w') as html_doc:
            html_doc.write(relative_to_absolute(http_response.text, f'http://{url.hostname}'))

        https_response = requests.get(f'https://{domain}/',
                                      timeout=timeout,
                                      headers={'User-Agent': user_agent})
        sanitized_url = sanitizer(f'https://{domain}/')
        html_session = \
            {
                'file_name': sanitized_url,
                'url': f'https://{domain}',
                'domain': f'{domain}',
                'status_code': https_response.status_code,
                'headers': dict(https_response.headers),

            }
        session_json.append(html_session)

        with open(f'{path_to_save}/hydra_report/response_body/{sanitized_url}.html', 'w') as html_doc:
            html_doc.write(relative_to_absolute(https_response.text, f'https://{url.hostname}'))

        print(f'[#] {domain} -> {url.scheme}://{url.hostname} :: {http_response.status_code}')
    except requests.ConnectionError:
        pass
    except requests.exceptions.ReadTimeout:
        print(f'[#] {domain} -> ReadTimeout Error')
    except KeyboardInterrupt:
        exit('Bye!')
    return json.dumps(response)


def save_session(path):
    with open(f'{path}/hydra_report/session.json', 'a') as session:
        session.write(json.dumps(session_json))
