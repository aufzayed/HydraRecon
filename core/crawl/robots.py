#!/usr/bin/env python3
import requests

USER_AGENT = 'Mozilla/5.0 (Windows NT 6.3; Win64; x64; rv:76.0) Gecko/20100101 Firefox/76.0'


def robots(domain):
    try:
        req = requests.get(f'https://{domain}/robots.txt', headers={'User-Agent': USER_AGENT})
        lines = req.text.split('\n')
        for line in lines:
            if line.startswith('Allow') or line.startswith('Disallow'):
                try:
                    path = line.split(' ')[1]
                    if path.startswith('/'):
                        yield f'https://{domain}{path}'
                    elif not path.startswith('/'):
                        yield f'https://{domain}/{path}'
                    elif path.startswith('https://') or path.startswith('http://'):
                        yield path
                    else:
                        pass
                except Exception:
                    pass
            elif line.startswith('Sitemap'):
                sitemap = line.split(' ')[1]
                yield sitemap
            else:
                pass
    except requests.ConnectionError:
        pass
