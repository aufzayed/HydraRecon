#!/usr/bin/env python3
from sys import exit
import json
import requests


def enumerator(target):
    domains = []
    try:

        response = requests.get('https://certspotter.com/api/v0/certs', params={'domain': target})
        json_response = json.loads(response.text)
        for domain_info in json_response:
            for domain in domain_info['dns_names']:
                domains.append(domain)
        return set(domains)
    except json.decoder.JSONDecodeError:
        pass
    except requests.ConnectionError:
        pass
    except TypeError:
        pass
    except KeyboardInterrupt:
        exit('Bye!')
