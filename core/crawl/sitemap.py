#!/usr/bin/env python3
import re
from sys import exit
import requests
from bs4 import BeautifulSoup as bsoup


def get_sitemap(your_input):
    domain_pattern = '[a-zA-Z0-9\.]+\.[a-zA-z]+'
    url_patterns = \
        '''
            (
                http[s]*\:\/\/[a-zA-Z0-9\.]*\/sitemap.xml
                |
                http[s]*\:\/\/[a-zA-Z0-9\.]*\/sitemaps\/sitemap.xml
                |
                http[s]*\:\/\/[a-zA-Z0-9\.]*\/[a-zA-Z0-9\/]*sitemap.xml
                |
                http[s]*\:\/\/[a-zA-Z0-9\.]*\/[a-zA-Z0-9\/]*[a-zA-Z0-9].*.xml
            )
        '''
    regex = re.compile(url_patterns, re.VERBOSE)
    if re.match(regex, your_input):
        try:
            sitemap_xml = requests.get(your_input)
            if sitemap_xml.status_code == 200:
                return sitemap_xml.text
            else:
                return 0
        except requests.ConnectionError:
            pass
        except KeyboardInterrupt:
            exit('Bye!')
    elif re.match(domain_pattern, your_input):
        try:
            sitemap_xml = requests.get(f'http://{your_input}/sitemap.xml')
            if sitemap_xml.status_code == 200:
                return sitemap_xml.text
            elif sitemap_xml.status_code != 200:
                sitemaps_xml = requests.get(f'https://{your_input}/sitemaps/sitemap.xml')
                return sitemaps_xml.text
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
    with open(f'{path}/hydra_report/crawler/sitemap_urls.txt', 'w') as results:
        for url in sitemap_urls:
            results.write(f'{url}\n')
