#!/usr/bin/env python3
import os
from bs4 import BeautifulSoup


def relative_to_absolute(file, domain):
    parser = BeautifulSoup(file, 'html.parser')
    imgs = parser.find_all('img')
    links = parser.find_all('link')
    scripts = parser.find_all('script')

    # manipulate script tags src
    for script in scripts:
        if script.get('src'):
            if script['src'].startswith('http://') | script['src'].startswith(
                    'https://'):
                pass
            elif script['src'].startswith('//'):
                script['src'] = f'http:{script["src"]}'
            else:
                script['src'] = f'{domain}{script["src"]}'
        else:
            pass

    # manipulate link tags src
    for link in links:
        if link.get('href'):
            if link['href'].startswith('//') | link['href'].startswith('http://') | link['href'].startswith(
                    'https://'):
                pass
            else:
                link['href'] = f'{domain}{link["href"]}'

    # manipulate img tags src
    for img in imgs:
        if img.get('src'):
            if img['src'].startswith('//') | img['src'].startswith('http://') | img['src'].startswith(
                    'https://') | \
                    img['src'].startswith('data:'):
                pass
            else:
                img['src'] = f'{domain}{img["src"]}'

    return parser.prettify()


# convert url to storable file name
def sanitizer(string):
    letters_to_escape = ['/', ':', '.']
    final_str = []
    for letter in string:
        if letter in letters_to_escape:
            letter = '_'
            final_str.append(letter)
        else:
            final_str.append(letter)
    return ''.join(final_str)
