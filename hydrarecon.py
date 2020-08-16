import os
import sys
import time
import json
import argparse
import itertools
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from urllib.parse import urlparse
from colorama import init, Fore
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
from core.crawl.gurl import common_crawl
from core.crawl.gurl import wayback
from core.crawl.gurl import url_scan
from core.crawl.gurl import virus_total
from core.crawl import jsparser
from core.crawl import robots
from core.crawl import sitemap

init()


def banner():
    print(Fore.GREEN + '''
               __           
|__|   _| _ _ |__)_ _ _  _  
|  |\/(_|| (_|| \(-(_(_)| ) 
    /                       
Made with ♥ by Abdelrhman(@aufzayed)
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

parser = argparse.ArgumentParser(usage=Fore.BLUE + '\n\nhydrarecon Methods:'
                                       '\n\t1.basic :: '
                                       '\n\t\t- subdomain enumeration'
                                       '\n\t\t- scan common ports'
                                       '\n\t\t- screenshot hosts'
                                       '\n\t\t- html report'
                                       '\n\t2.crawl :: '
                                       '\n\t\t- sitemap.xml'
                                       '\n\t\t- robots.txt'
                                       '\n\t\t- related urls'
                                       '\n\t3.config :: config hydra\n\n'
                                       'examples:'
                                       '\n\tpython3 hydrarecon.py --basic -d example.com'
                                       '\n\tpython3 hydrarecon.py --crawl -d example.com'
                                       '\n\tpython3 hydrarecon.py --config')

parser.add_argument('--basic', help='use basic recon module', action='store_true')
parser.add_argument('--crawl', help='use crawl module', action='store_true')
parser.add_argument('--config', help='initializing config file', action='store_true')
parser.add_argument('--session', help='Generate report from session.json file', action='store_true')
parser.add_argument('-d', '--domain', metavar='', help='domain to crawl or recon')
parser.add_argument('-p', '--ports', metavar='', help='ports to scan: (small | large | xlarge). default: small',
                    default='small')
parser.add_argument('-T', '--timeout', metavar='', help='control http request timeout in seconds, default: 1s',
                    default=1, type=int)
parser.add_argument('-t', '--threads', metavar='', help='number of threads, default: 10', default=10, type=int)
parser.add_argument('-o', '--out', metavar='', help='path to save report, default : home directory')

args = parser.parse_args()


def check_domain_input(domain):
    if domain.startswith('https://') or domain.startswith('http://'):
        url_parse = urlparse(domain)
        return url_parse.hostname
    else:
        return domain


def init_hydra_report(path):
    print(Fore.BLUE + f'[#] {Fore.GREEN}initializing HydraRecon report')
    try:
        os.mkdir(f'{path}/hydra_report')
        os.mkdir(f'{path}/hydra_report/response_body')
        os.mkdir(f'{path}/hydra_report/screenshots')
        os.mkdir(f'{path}/hydra_report/crawler')
    except FileExistsError:
        pass


def subdomain_enum(domain, path):
    subdomains = set()
    print(Fore.BLUE + f'[#] {Fore.GREEN}Collecting Subdomains')
    time.sleep(1)
    print(f'{Fore.BLUE} | certspotter API')
    _cs = certspotter.enumerator(domain)
    print(f'{Fore.BLUE} | crt.sh API')
    _crt = crtsh.enumerator(domain, depth=5)
    print(f'{Fore.BLUE} | bufferover API')
    _dbo = dnsbufferover.enumerator(domain)
    print(f'{Fore.BLUE} | entrust API')
    _et = entrust.enumerator(domain)
    print(f'{Fore.BLUE} | hackertarget API')
    _ht = hackertarget.enumerator(domain)
    print(f'{Fore.BLUE} | threatcrowd API')
    _tc = threatcrowd.enumerator(domain)
    print(f'{Fore.BLUE} | threatminer API')
    _tm = threatminer.enumerator(domain)
    print(f'{Fore.BLUE} | urlscan API')
    _us = urlscan.enumerator(domain)
    print(f'{Fore.BLUE} | virustotal API')
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
    print(Fore.BLUE + f'[#] {Fore.GREEN}Checking subdomains')
    with open(f'{path}/hydra_report/subs.{domain}.txt') as domains:
        with ThreadPoolExecutor(max_workers=threads) as executor:
            for domain in domains:
                domain = domain.split('\n')[0]
                executor.submit(httprobe.probe, domain, path, timeout=timeout)


def take_screenshot(path):
    print(Fore.BLUE + f'[#] {Fore.GREEN}Take Screenshot for subdomains')
    time.sleep(1)
    screenshot.screenshot(path)


def parse_js(path, threads):
    print(Fore.BLUE + f'[#] {Fore.GREEN}Parsing Javascript Files')
    js_links = jsparser.get_links(f'{path}/hydra_report/response_body')
    with ThreadPoolExecutor(max_workers=threads) as executor:
        for link in js_links:
            executor.submit(jsparser.js_parser, link)
    jsparser.save(path)


def gurl_crawler(path, domain):
    print(Fore.BLUE + f'[#] {Fore.GREEN}Get {domain} urls')
    print(f'{Fore.BLUE} | wayback API')
    _wb_crawler = wayback.api(domain)
    print(f'{Fore.BLUE} | common crawl API')
    _cc_crawler = common_crawl.api(domain)
    print(f'{Fore.BLUE} | urlscan API')
    _us_crawler = url_scan.api(domain)
    print(f'{Fore.BLUE} | virustotal API')
    _vt_crawler = virus_total.api(domain)
    with open(f'{path}/hydra_report/crawler/{domain}.urls.txt', 'a') as wb_urls:
        for url in itertools.chain(_wb_crawler, common_crawl.URLs, _us_crawler, _vt_crawler):
            wb_urls.write(f'{url}\n')


def crawl_robots(path, threads,  domain):
    print(Fore.BLUE + f'[#] {Fore.GREEN}Collecting {domain} robots.txt urls')
    with open(f'{path}/hydra_report/session.json') as session:
        hosts = json.load(session)
        with ThreadPoolExecutor(max_workers=threads) as executor:
            for h in hosts:
                executor.submit(robots.robots, h['url'])
    robots.save(path)


def crawl_sitemap(path, threads, domain):
    print(Fore.BLUE + f'[#] {Fore.GREEN}Collecting {domain} sitemap urls')
    with open(f'{path}/hydra_report/session.json') as session:
        hosts = json.load(session)
        with ThreadPoolExecutor(max_workers=threads) as executor:
            for h in hosts:
                executor.submit(sitemap.get_urls, h['domain'])
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

# check if provided domain is clear or not
# if domain is provided with http schema
# the check_domain_input will remove it and return hostname
try:
    host = check_domain_input(args.domain)
except AttributeError:
    pass

if not args.basic and not args.crawl and not args.session and not args.config:
    print(Fore.RED + '[!] Please Choose Method')
    sys.exit()
elif args.session:
    if args.out is None:
        path_to_save = HOME_PATH
    else:
        path_to_save = os.path.abspath(args.out)
    take_screenshot(path_to_save)
    report_generator.render(path_to_save)

elif args.basic and not args.crawl:
    if args.out is None:
        path_to_save = HOME_PATH
    else:
        path_to_save = os.path.abspath(args.out)

    init_hydra_report(path_to_save)
    subdomain_enum(host, path_to_save)
    probe(host, args.threads, path_to_save, timeout=args.timeout)
    httprobe.save_session(path_to_save)
    take_screenshot(path_to_save)
    portscanner.scan(host, args.threads, ports_range=args.ports, path=path_to_save)
    report_generator.render(path_to_save)

elif not args.basic and args.crawl:
    if args.out is None:
        path_to_save = HOME_PATH
    else:
        path_to_save = args.out

    parse_js(path_to_save, args.threads)
    gurl_crawler(path_to_save, host)
    crawl_robots(path_to_save, args.threads, host)
    crawl_sitemap(path_to_save, args.threads,  host)
else:
    pass
