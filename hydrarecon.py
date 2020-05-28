import os
import sys
import time
import json
import argparse
import itertools
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from core.basic import httprobe
from core.basic import screenshot
from core.basic import portscanner
from core.basic.subenum import certspotter
from core.basic.subenum import crtsh
from core.basic.subenum import dnsbufferover
from core.basic.subenum import entrust
from core.basic.subenum import hackertarget
from core.basic.subenum import threatcrowd
from core.basic.subenum import threatminer
from core.basic.subenum import urlscan
from core.basic.subenum import virustotal
from core.basic.report import report_generator
from core.crawl import gurl
from core.crawl import jsparser
from core.crawl import robots
from core.crawl import sitemap


def banner():
    print('''
               __           
|__|   _| _ _ |__)_ _ _  _  
|  |\/(_|| (_|| \(-(_(_)| ) 
    /                       

''')


banner()

HOME_PATH = Path.home()

try:
    with open(f'{HOME_PATH}/.hydra_config.json') as hydra_config:
        try:
            key = json.load(hydra_config)
            VTOTAL_KEY = key['vtotal_key']
        except json.JSONDecodeError as e:
            print(e)
            VTOTAL_KEY = None
except FileNotFoundError:
    VTOTAL_KEY = None
    pass

parser = argparse.ArgumentParser(usage='\n\nhydrarecon Methods:'
                                       '\n\t1.basic :: '
                                       '\n\t\t- subdomain enumeration'
                                       '\n\t\t- scan common ports'
                                       '\n\t\t- screenshot hosts'
                                       '\n\t\t- html report'
                                       '\n\t2.crawl :: '
                                       '\n\t\t- sitemap.xml'
                                       '\n\t\t- robots.txt'
                                       '\n\t\t- related urls: '
                                       '\n\t\t\t* wayback machine'
                                       '\n\t\t\t* virus total'
                                       '\n\t\t\t* common crawl'
                                       '\n\t\t\t* urlscan\n'
                                       '\n\t3.config :: config hydra\n\n'
                                       'examples:'
                                       '\n\tpython3 hydrarecon.py --basic -d example.com'
                                       '\n\tpython3 hydrarecon.py --crawl -d example.com'
                                       '\n\tpython3 hydrarecon.py --config')

parser.add_argument('--basic', help='use basic recon module', action='store_true')
parser.add_argument('--crawl', help='use crawl module', action='store_true')
parser.add_argument('--config', help='initializing config file', action='store_true')
parser.add_argument('--only-sub', help='subdoamin enumeration only', action='store_true')
parser.add_argument('-d', '--domain', metavar='', help='domain to crawl or recon')
parser.add_argument('-p', '--ports', metavar='', help='ports to scan: (small | large | xlarge). default: small',
                    default='small')
parser.add_argument('-T', '--timeout', metavar='', help='control http request timeout in seconds, default: 1s',
                    default=1, type=int)
parser.add_argument('-t', '--threads', metavar='', help='number of threads, default: 10', default=10, type=int)
parser.add_argument('-o', '--out', metavar='', help='path to save report, default : home directory')

args = parser.parse_args()


def init_hydra_report(path):
    print('[#] initializing HydraRecon report')
    try:
        os.mkdir(f'{path}/hydra_report')
        os.mkdir(f'{path}/hydra_report/response_body')
        os.mkdir(f'{path}/hydra_report/screenshots')
        os.mkdir(f'{path}/hydra_report/crawler')
    except FileExistsError:
        pass


def subdomain_enum(domain, path):
    subdomains = set()
    print('[#] Collecting Subdomains')
    time.sleep(1)
    print('[#] certspotter API')
    _cs = certspotter.enumerator(domain)
    print('[#] crt.sh API')
    _crt = crtsh.enumerator(domain, depth=5)
    print('[#] bufferover API')
    _dbo = dnsbufferover.enumerator(domain)
    print('[#] entrust API')
    _et = entrust.enumerator(domain)
    print('[#] hackertarget API')
    _ht = hackertarget.enumerator(domain)
    print('[#] threatcrowd API')
    _tc = threatcrowd.enumerator(domain)
    print('[#] threatminer API')
    _tm = threatminer.enumerator(domain)
    print('[#] urlscan API')
    _us = urlscan.enumerator(domain)
    print('[#] virustotal API')
    _vt = virustotal.enumerator(domain, apikey=VTOTAL_KEY)

    for subdomain in itertools.chain(_cs, _crt, _dbo, _et, _ht, _tc, _tm, _us, _vt):
        if subdomain.startswith('*'):
            subdomain = subdomain.split('*.')[1]
            if subdomain.endswith(f'.{domain}'):
                subdomains.add(subdomain)
        elif subdomain.endswith(f'.{domain}'):
            subdomains.add(subdomain)
        else:
            pass

    with open(f'{path}/hydra_report/subs.{domain}.txt', 'a') as subs_file:
        for sub in subdomains:
            subs_file.write(f'{sub}\n')


def probe(domain, threads, path, timeout):
    with open(f'{path}/hydra_report/subs.{domain}.txt') as domains:
        with ThreadPoolExecutor(max_workers=threads) as executor:
            for domain in domains:
                domain = domain.split('\n')[0]
                executor.submit(httprobe.probe, domain, path, timeout=timeout)


def take_screenshot(path):
    print('[#] Take Screenshot for subdomains')
    time.sleep(1)
    screenshot.screenshot(path)


def parse_js(path, threads):
    print('[#] Parsing Javascript Files')
    js_links = jsparser.get_links(f'{path}/hydra_report/response_body')
    with ThreadPoolExecutor(max_workers=threads) as executor:
        for link in js_links:
            executor.submit(jsparser.js_parser, link)
    jsparser.save(path)


def gurl_crawler(path, domain):
    print(f'[#] Collecting {domain} urls from wayback machine')
    _wb_crawler = gurl.wayback_machine(domain)
    print(f'[#] Collecting {domain} urls from common crawl')
    _cc_crawler = gurl.common_crawl(domain)
    print(f'[#] Collecting {domain} urls from url scan')
    _us_crawler = gurl.url_scan(domain)
    print(f'[#] Collecting {domain} urls from virus total')
    _vt_crawler = gurl.virus_total(domain)
    with open(f'{path}/hydra_report/crawler/{domain}.wayback.txt', 'a') as wb_urls:
        for url in itertools.chain(_wb_crawler, _cc_crawler, _us_crawler, _vt_crawler):
            wb_urls.write(f'{url}\n')


def crawl_robots(path, threads,  domain):
    print(f'[#] Collecting {domain} robots.txt urls')
    with open(f'{path}/hydra_report/session.json') as session:
        hosts = json.load(session)
        with ThreadPoolExecutor(max_workers=threads) as executor:
            for host in hosts:
                executor.submit(robots.robots, host['url'])
    robots.save(path)


def crawl_sitemap(path, threads, domain):
    print(f'[#] Collecting {domain} sitemap urls')
    with open(f'{path}/hydra_report/session.json') as session:
        hosts = json.load(session)
        with ThreadPoolExecutor(max_workers=threads) as executor:
            for host in hosts:
                executor.submit(sitemap.get_urls, host)
    sitemap.save(path)


if args.config:
    enter_key = input('Hydra needs virus total API key, do you have a key [y/n]: ')
    if enter_key.lower() == 'y':
        key = input('Please Enter Key: ')
        if len(key) == 64:
            with open(f'{HOME_PATH}/.hydra_config.json', 'w') as config:
                json_config = json.dumps({"vtotal_key": key})
                config.write(json_config)
                print(f'[*] config file: {HOME_PATH}/.hydra_config.json')
            sys.exit()
        else:
            print('[!] wrong key')
            sys.exit()
    elif enter_key.lower() == 'n':
        print('[!] virus total module will not work')
        sys.exit()
    else:
        sys.exit()
else:
    pass

if not args.basic and not args.crawl:
    print('Please Choose a Method')
    sys.exit()
elif args.basic and not args.crawl:
    if args.out is None:
        path_to_save = HOME_PATH
    else:
        path_to_save = os.path.abspath(args.out)

    if args.threads == 10:
        workers = 10
    else:
        workers = args.threads

    if args.timeout == 1:
        time_out = args.timeout
    else:
        time_out = args.timeout

    init_hydra_report(path_to_save)
    subdomain_enum(args.domain, path_to_save)
    probe(args.domain, workers, path_to_save, timeout=time_out)
    httprobe.save_session(path_to_save)
    take_screenshot(path_to_save)
    portscanner.scan(args.domain, workers, ports_range=args.ports, path=path_to_save)
    report_generator.render(path_to_save)

elif not args.basic and args.crawl:
    if args.out is None:
        path_to_save = HOME_PATH
    else:
        path_to_save = args.out

    if args.threads == 10:
        workers = 10
    else:
        workers = args.threads

    parse_js(path_to_save, workers)
    gurl_crawler(path_to_save, args.domain)
    crawl_robots(path_to_save, workers, args.domain)
    crawl_sitemap(path_to_save, workers,  args.domain)
else:
    pass