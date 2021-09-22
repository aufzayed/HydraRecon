#!/usr/bin/env python3
from sys import exit
import requests
from bs4 import BeautifulSoup as bsoup


def get_sitemap(domain):
    try:
        sitemap_xml = requests.get(f'http://{domain}/sitemap.xml')
        if sitemap_xml.status_code == 200:
            return sitemap_xml.text
        elif sitemap_xml.status_code != 200:
            sitemap_xml = requests.get(f'http://{domain}/sitemaps/sitemap.xml')
            return sitemap_xml
        else:
            return 0
    except requests.ConnectionError:
        pass
    except KeyboardInterrupt:
        exit('Bye!')


def xml_parse(domain):
    try:
        sitemap_xml = bsoup(get_sitemap(domain), 'lxml')
        urls = sitemap_xml.find_all('loc')
        for url in urls:
            yield url.string
    except Exception:
        pass
    except KeyboardInterrupt:
        exit('Bye!')


sitemap_urls = set()


def get_urls(domain):
    for url in xml_parse(domain):
        if url.endswith('.xml'):
            for u in xml_parse(url):
                sitemap_urls.add(u)
        else:
            sitemap_urls.add(url)
    return


def save(path):
    with open(f'{path}/hydra_report/crawler/sitemap_urls.txt', 'a') as results:
        for url in sitemap_urls:
            results.write(f'{url}\n')
