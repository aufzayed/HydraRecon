#!/usr/bin/env python3
import requests


def hackertraget_api(hostname):
    try:
        response = requests.get('https://api.hackertarget.com/hostsearch/', params={'q': hostname})
        domains = [i.split(',')[0] for i in response.text.split('\n')]
        return set(domains)
    except Exception as e:
        print(f'[!][hackertraget] Runtime Error: {e}')
        return []
