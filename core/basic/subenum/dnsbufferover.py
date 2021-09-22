#!/usr/bin/env python3
import requests


def dnsbufferover_api(hostname):
    domains = []
    try:
        response = requests.get('https://dns.bufferover.run/dns', params={'q': hostname})
        buffer_response = response.json()

        fdns = [d.split(',')[1] for d in buffer_response['FDNS_A']]
        domains.extend(fdns)

        rdns = [d.split(',')[1] for d in buffer_response['RDNS']]
        domains.extend(rdns)

    except Exception as e:
        print(f'[!][dnsbufferover] Runtime Error {e}')
    return set(domains)
