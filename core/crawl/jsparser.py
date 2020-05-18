#!/usr/bin/env python3
import os
import re
from sys import exit
from urllib.parse import urlparse
import requests
from bs4 import BeautifulSoup
from core.crawl.regex import endpoints_regex


def get_links(path):
    js_links = set()
    files = os.listdir(path)
    for file in files:
        file_path = f'{path}/{file}'
        with open(file_path) as html_file:
            html_parser = BeautifulSoup(html_file, 'html.parser')
            scripts = html_parser.find_all('script')
            for tag in scripts:
                if tag.get('src') is not None:
                    js_links.add(tag.get('src'))
    return js_links


found_endpoints = set()


def js_parser(link):
    find_endpoints = re.compile(endpoints_regex, re.VERBOSE)
    try:
        response = requests.get(link)
        endpoints = find_endpoints.findall(response.text)
        host = urlparse(response.url)
        for e in endpoints:
            for i in e:
                if i != '':
                    if i[0:8] == 'http://' or i[0:9] == 'https://':
                        found_endpoints.add(i)
                    elif i[0:2] == '//':
                        found_endpoints.add(f'http:{i}')
                    elif i[0] == '/' and i[1] != '/':
                        found_endpoints.add(f'{host.scheme}://{host.hostname}{i}')
                    elif i[0] == '.':
                        found_endpoints.add(f'{host.scheme}://{host.hostname}/{i}')
    except requests.ConnectionError:
        pass
    except KeyboardInterrupt:
        exit('Bye!')


def save(path):
    with open(f'{path}/hydra_report/crawler/js_parser_results.txt', 'a') as results:
        for i in found_endpoints:
            results.write(f'{i}\n')
