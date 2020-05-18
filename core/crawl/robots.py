#!/usr/bin/env python3
from sys import exit
import requests

USER_AGENT = 'Mozilla/5.0 (Windows NT 6.3; Win64; x64; rv:76.0) Gecko/20100101 Firefox/76.0'

robots_urls = set()


def robots(domain):
    try:
        req = requests.get(f'{domain}/robots.txt', headers={'User-Agent': USER_AGENT})
        lines = req.text.split('\n')
        for line in lines:
            if line[0:6] == 'Allow' or line[0:9] == 'Disallow':
                try:
                    path = line.split(' ')[1]
                    if path[0] == '/' and path[1] != '/':
                        robots_urls.add(f'{domain}{path}')
                    elif path[0] != '/':
                        robots_urls.add(f'{domain}/{path}')
                    elif path[0:8] == 'http://' or path[0:9] == 'https://':
                        robots_urls.add(path)
                    else:
                        pass
                except Exception as e:
                    print(f'[#] Runtime Exception {e}')
                except KeyboardInterrupt:
                    exit('Bye!')
            elif line[0:8] == 'Sitemap':
                sitemap = line.split(' ')[1]
                robots_urls.add(sitemap)
            else:
                pass
    except requests.ConnectionError:
        pass
    except KeyboardInterrupt:
        exit('Bye!')


def save(path):
    with open(f'{path}/hydra_report/crawler/robots_urls.txt', 'w') as results:
        for url in robots_urls:
            results.write(f'{url}\n')
