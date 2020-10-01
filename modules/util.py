#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import requests
from requests.exceptions import HTTPError
from bs4 import BeautifulSoup
from itertools import cycle
from lxml.html import fromstring
from key import *
from datetime import datetime


def data_login():
    import getpass
    data = [input("Type your user login:  ")]
    try:
        data.append(getpass.getpass(prompt='Type your password login: '))
    except Exception as error:
        print('ERROR', error)
    return data

def get_proxy_pool():
    url = 'http://falcon.proxyrotator.com:51337/proxy-list/?apiKey=' + code_apiKey_proxyrotator
    response = requests.get(url)
    parser = fromstring(response.text)
    proxylist = response.text.split()
    proxies = set()
    for proxy in proxylist:
        proxies.add(proxy)
    pool = cycle(proxies)
    return pool


def proxy_rotator():
    api_key = ''
    resp = requests.get(url='http://falcon.proxyrotator.com:51337/',
                        params=dict(apiKey=code_apiKey_proxyrotator))
    data = json.loads(resp.text)
    return data


def request(url, proxy=False):
    try:
        if proxy:
            proxyrotator = proxy_rotator()
            proxies = {'http': 'http://' + proxyrotator['proxy'],
                       'https': 'http://' + proxyrotator['proxy']}
            headers = {'User-Agent': proxyrotator['randomUserAgent']}
            print('PROXIES: YES BRO!!')
            response = requests.get(url, proxies=proxies, headers=headers)
        else:
            print('NO PROXIES BUDY :´(')
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Safari/537.36'}
            response = requests.get(url, timeout=4, headers=headers)
        response.raise_for_status()  # If the response was successful, no Exception will be raised
        return response.content, response.status_code
    except HTTPError as http_err:
        print('---> HTTP error occurred: ' + str(http_err))
        exit(1)
    except Exception as err:
        print('+++> Other error occurred: ' + str(err))
        exit(1)


def get_soup_packtpage(content):
    soup_packtpage = ''
    try:
        soup_packtpage = BeautifulSoup(content, 'lxml')
        return soup_packtpage
    except Exception as err:
        print('>> Error occurred (get_soup_packtpage): ' + str(err))
        exit(0)


def get_canonical(soup_packtpage):
    """
    get_canonical:
    comprueba que la pagina que quiero scrapear sea la pagina que he enviado.
    en productos muy antiguos ya no existe la pagina el productoV pero si su url y
    te envia a una pagina de listado de productos genérica
    """
    canonical = soup_packtpage.find("link", rel="canonical")
    if canonical:
        canonical_url = canonical['href']
    else:
        canonical_url = ''
    return canonical_url


def print_dict(dic, clave):
    from tabulate import tabulate

    new_dicc = {clave: [], 'URL': []}
    for k, v in dic.items():
        new_dicc[clave].append(k)
        new_dicc['URL'].append(v)
    print(tabulate(new_dicc, headers=[clave, 'URL'], showindex=True))


def platform_system():
    """
    Return the platform_system platform of machine
    """
    import platform
    return platform.system()


