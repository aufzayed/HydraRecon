#!/usr/bin/env python3
from sys import exit
import json
import requests


def enumerator(domain):
    domains = []
    try:
        response = requests.get('https://api.threatminer.org/v2/domain.php', params={'q': domain, 'rt': 5})
        json_response = json.loads(response.text)
        for d in json_response['results']:
            domains.append(d)
    except requests.ConnectionError:
        pass
    except json.decoder.JSONDecodeError:
        pass
    except KeyboardInterrupt:
        exit('Bye!')
    return set(domains)
