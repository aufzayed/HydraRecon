#!/usr/bin/env python3
import requests


def crobat_api(hostname):
    try:
        res = requests.get(f'https://sonar.omnisint.io/subdomains/{hostname}')
        domains_list = [d for d in res.json()]
        return domains_list
    except Exception as e:
        print(f'[!][crobat] Runtime Error: {e}')
        return []
