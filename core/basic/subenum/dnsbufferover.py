#!/usr/bin/env python3
import json
import requests


def enumerator(domain):
    domains = []
    try:
        response = requests.get('https://dns.bufferover.run/dns', params={'q': domain})
        buffer_response = json.loads(response.text)
        try:
            for i in buffer_response['FDNS_A']:
                try:
                    domains.append(i.split(',')[1])
                except IndexError:
                    domains.append(i)
        except TypeError:
            pass
        try:
            for i in buffer_response['RDNS']:
                try:
                    domains.append(i.split(',')[1])
                except IndexError:
                    domains.append(i)
        except TypeError:
            pass
    except json.decoder.JSONDecodeError:
        pass
    except requests.ConnectionError:
        pass
    return set(domains)
