#!/usr/bin/env python3
from sys import exit
import requests


def enumerator(domain):
    domains = []
    try:
        response = requests.get('https://api.hackertarget.com/hostsearch/', params={'q': domain})
        for i in response.text.split('\n'):
            domains.append(i.split(',')[0])
    except requests.ConnectionError:
        pass
    except KeyboardInterrupt:
        exit('Bye!')
    return set(domains)
