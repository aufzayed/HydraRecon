#!/usr/bin/evn python3
import json
import requests


def requester(domain, depth=1):
    depth = '%.' * depth
    try:
        parameters = {'q': f'{depth}{domain}', 'output': 'json'}
        response = requests.get('https://crt.sh', params=parameters)
        if response.text is not None:
            return response.text
    except requests.ConnectionError:
        pass


def enumerator(domain, depth):
    domains = []
    while depth >= 0:
        try:
            json_domains = json.loads(requester(domain, depth=depth))
            for i in json_domains:
                i = i['name_value']
                if i != '':
                    domains_list = i.split('\n')
                    if isinstance(domains_list, list):
                        for d in domains_list:
                            domains.append(d)
                    else:
                        domains.append(i)
                else:
                    pass
        except json.decoder.JSONDecodeError:
            pass

        depth -= 1
    else:
        pass
    return set(domains)
