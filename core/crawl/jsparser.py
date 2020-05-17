#!/usr/bin/evn python3
from core.crawl.regex import *

import os
import re
import requests
from bs4 import BeautifulSoup

from core.basic.helpers import sanitizer, relative_to_absolute


def js_parser(domain, path):
    re_endpoints = re.compile(endpoints_regex, re.VERBOSE)  # re to match endpoints
    re_secrets = re.compile(secrets_regex, re.VERBOSE)  # re to match secrets
    response = requests.get(f'http://{domain}/')
    name = sanitizer(response.url)
    template = {name: {'secrets': set(), 'endpoints': set()}}
    print(f'[#] Parsing {name}')
    html_parser = BeautifulSoup(relative_to_absolute(response.text, response.url), 'html.parser')
    scripts = html_parser.find_all('script')
    for tag in scripts:
        src = tag.get('src')
        # find endpoints and secrets in js files
        if src is not None:
            # load js files
            try:
                load_js = requests.get(src).text

                match_endpoints = re_endpoints.findall(load_js)
                for end in match_endpoints:
                    for i in end:
                        if i != '':
                            template[name]['endpoints'].add(i)
                match_secrets = re_secrets.findall(load_js)
                for sec in match_secrets:
                    template[name]['secrets'].add(sec)
            except requests.ConnectionError:
                pass
        # find endpoints and secrets in script tags
        elif src is None:
            code = tag.string
            try:
                match_endpoints = re_endpoints.findall(code)
                for end in match_endpoints:
                    for i in end:
                        if i != '':
                            template[name]['endpoints'].add(i)
                match_secrets = re_secrets.findall(code)
                for sec in match_secrets:
                    template[name]['secrets'].add(sec)
            except TypeError:
                pass
    save_path = f'{path}/hydra_report/crawler/js_parser_results/'
    file_name = list(template.keys())[0]
    try:
        os.mkdir(f'{save_path}{file_name}')
    except FileExistsError:
        pass
    with open(f'{save_path}{file_name}/endpoints.txt', 'a') as ends:
        for k in template.keys():
            for i in template[k]['endpoints']:
                ends.write(f'{i}\n')
    with open(f'{save_path}{file_name}/secrets.txt', 'a') as secrets:
        for k in template.keys():
            for i in template[k]['secrets']:
                secrets.write(f'{i}\n')

