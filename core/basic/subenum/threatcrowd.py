#!/usr/bin/env python3
from sys import exit
import json
import requests


def enumerator(domain):
    domains = []
    try:
        response = requests.get('https://www.threatcrowd.org/searchApi/v2/domain/report/', params={'domain': domain})
        json_response = json.loads(response.text)
        try:
            for domain in json_response['subdomains']:
                domains.append(domain)
        except KeyError:
            pass
    except requests.ConnectionError:
        pass
    except json.decoder.JSONDecodeError:
        pass
    except KeyboardInterrupt:
        exit('Bye!')
    return set(domains)

