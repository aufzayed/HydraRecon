#!/usr/bin/env python3
import socket
from sys import exit
from concurrent.futures import ThreadPoolExecutor

scanner_results = set()


def port_scanner(host, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as scanner:
        try:
            scanner.settimeout(1)
            result = scanner.connect_ex((host, port))
            if result == 0:
                scanner_results.add(f'{host}:{port}')
            else:
                pass
        except socket.gaierror:
            pass
        except KeyboardInterrupt:
            exit('Bye!')


xlarge = ("81", "300", "591", "593", "832", "981", "1010", "1311", "2082", "2087", "2095",
          "2096", "2480", "3000", "3128", "3333", "4243", "4567", "4711", "4712", "4993",
          "5000", "5104", "5108", "5800", "6543", "7000", "7396", "7474", "8000", "8001",
          "8008", "8014", "8042", "8069", "8080", "8081", "8088", "8090", "8091", "8118",
          "8123", "8172", "8222", "8243", "8280", "8281", "8333", "8443", "8444", "8445",
          "8500", "8834", "8880", "8888", "8983", "9000", "9043", "9060", "9080", "9090",
          "9091", "9200", "9443", "9800", "9981", "12443", "16080", "18091", "18092", "20720", "28017")

large = ("81", "591", "2082", "2087", "2095", "2096", "3000", "8000", "8001", "8008", "8080",
         "8083", "8443", "8834", "8888")

small = ("80", "443", "8080", "8443")


def scan(domain, threads, ports_range='small', path=None):
    if ports_range == 'small':
        ports_range = small
    elif ports_range == 'large':
        ports_range = large
    elif ports_range == 'xlarge':
        ports_range = xlarge

    if path is not None:
        print('[#] Port Scanning...')
        with open(f'{path}/hydra_report/subs.{domain}.txt') as hosts:
            with ThreadPoolExecutor(max_workers=threads) as executor:
                for host in hosts:
                    host = host.split('\n')[0]
                    for port in ports_range:
                        executor.submit(port_scanner, host, int(port))
    else:
        pass
    print('[#] Port Scanning Done!')
    if len(scanner_results) != 0:
        with open(f'{path}/hydra_report/port_scanner_results.txt', 'a') as results:
            for i in scanner_results:
                results.write(f'{i}\n')
    else:
        pass
