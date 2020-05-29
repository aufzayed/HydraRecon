#!/usr/bin/env python3
import os
from bs4 import BeautifulSoup


def rel_to_abs(doc, domain):
    parser = BeautifulSoup(doc, 'html.parser')
    scripts = parser.find_all('script')
    links = parser.find_all('link')
    imgs = parser.find_all('img')

    # remove csp
    meta = parser.find_all('meta')
    for m in meta:
        csp = m.get('http-equiv')
        if csp == 'Content-Security-Policy':
            del m['content']
            del m['http-equiv']

    for s in scripts:
        src = s.get("src")
        if src is not None:
            if src[0:8] == 'https://' or src[0:7] == 'http://':
                s['src'] = src
            elif src[0:2] == "//":
                s['src'] = f'http:{src}'
            elif src[0] == '/' and src[1] != '/':
                s['src'] = f'http://{domain}{src}'
            elif src[0] == '.':
                s['src'] = f'http://{domain}/{src}'
            elif src[0] != '.' or src[0] != '/' or src[0:7] != 'http://' or src[0:8] != 'https://':
                s['src'] = f'http://{domain}/{src}'

    for l in links:
        href = l.get('href')
        if href is not None:
            if href[0:8] == 'https://' or href[0:7] == 'http://':
                l['href'] = href
            elif href[0:2] == "//":
                l['href'] = f'http:{href}'
            elif href[0] == '/' and href[1] != '/':
                l['href'] = f'http://{domain}{href}'
            elif href[0] == '.':
                l['href'] = f'http://{domain}/{href}'
            elif href[0] != '.' or href[0] != '/' or href[0:7] != 'http://' or href[0:8] != 'https://':
                l['href'] = f'http://{domain}/{href}'

    for i in imgs:
        isrc = i.get('src')
        if isrc is not None:
            if isrc[0:8] == 'https://' or isrc[0:7] == 'http://' or isrc[0:5] == 'data:':
                i['src'] = isrc
            elif isrc[0:2] == "//":
                i['src'] = f'http:{isrc}'
            elif isrc[0] == '/' and isrc[1] != '/':
                i['src'] = f'http://{domain}{isrc}'
            elif isrc[0] == '.':
                i['src'] = f'http://{domain}/{isrc}'
            elif isrc[0] != '.' or isrc[0] != '/' or isrc[0:7] != 'http://' or isrc[0:8] != 'https://' or isrc[0:5] != 'data:':
                i['src'] = f'http://{domain}/{isrc}'
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
