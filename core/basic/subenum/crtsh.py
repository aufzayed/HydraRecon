#!/usr/bin/evn python3
import requests


def crtsh_api(hostname, depth):
    domain_list = []
    for i in range(int(depth)):
        try:
            _depth = '%.' * depth
            parameters = {'q': f'{_depth}{hostname}', 'output': 'json'}
            response = requests.get('https://crt.sh', params=parameters)
            domains = [domain for domain in response.json() for domain in domain['name_value'].split('\n')]
            domain_list.extend(domains)
        except Exception as e:
            print(f'[!][crt.sh] Runtime Error {e}')
    return set(domain_list)
