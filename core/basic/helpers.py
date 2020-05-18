#!/usr/bin/env python3
import os
from bs4 import BeautifulSoup


def relative_to_absolute(file, domain):
    parser = BeautifulSoup(file, 'html.parser')
    imgs = parser.find_all('img')
    links = parser.find_all('link')
    scripts = parser.find_all('script')

    for script in scripts:
        if script.get('src'):
            if script['src'][0:8] == 'http://' or script['src'][0:9] == 'https://':
                pass
            elif script['src'][0:2] == '//':
                script['src'] = f'http:{script["src"]}'
            elif script['src'][0] == '/' and script['src'][1] != '/':
                script['src'] = f'{domain}{script["src"]}'
            elif script['src'][0] != '/' and script['src'][0] != '.':
                script['src'] = f'{domain}/{script["src"]}'
        else:
            pass

    for link in links:
        if link.get('href'):
            if link['href'][0:2] == '//' or link['href'][0:8] == 'http://' or link['href'][0:9] == 'https://':
                pass
            elif link['href'][0] == '/' and link['src'][1] != '/':
                link['href'] = f'{domain}{link["href"]}'
            elif link['href'][0] == '.':
                link['href'] = f'{domain}{link["href"]}'

    for img in imgs:
        if img.get('src'):
            if img['src'][0:2] == '//' or img['src'][0:8] == 'http://' or img['src'][0:9] == 'https://' or img['src'][0:6] == 'data:':
                pass
            elif img['src'][0] == '/' and img['src'][1] != '/':
                img['src'] = f'{domain}{img["src"]}'
            elif img['src'][0] == '.':
                img['src'] = f'{domain}/{img["src"]}'

    return parser.prettify()


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
