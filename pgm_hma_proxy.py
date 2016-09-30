#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
import requests
import re
import sys
import logging
import configargparse

from queue import Queue
from threading import Thread

# ======================================================
logging.basicConfig(
    format='%(asctime)s %(levelname)s: %(message)s',
    datefmt='%H:%M:%S'
)
log = logging.getLogger(__name__)

# ======================================================
# Scrap Hyde my ass multi-pages
def scrapes_hma(pages):
    log.debug('Start getting HMA proxis, in %s page(s).', pages)
    
    proxies = []
    for i in range(1,pages):
            scrape_hma(str(i), proxies),

    log.debug('Ending, found %s proxies.', len(proxies))
    return(proxies)

# ======================================================
# Scrap Hyde My Ass ProxyList
def scrape_hma(page, proxies):
    
    r = requests.get('http://proxylist.hidemyass.com/'+page)
    bad_class="("
    for line in r.text.splitlines():
        class_name = re.search(r'\.([a-zA-Z0-9_\-]{4})\{display:none\}', line)
        if class_name is not None:
           bad_class += class_name.group(1)+'|'

    bad_class = bad_class.rstrip('|')
    bad_class += ')'

    to_remove = '(<span class\="'+ bad_class + '">[0-9]{1,3}</span>|<span style=\"display:(none|inline)\">[0-9]{1,3}</span>|<div style="display:none">[0-9]{1,3}</div>|<span class="[a-zA-Z0-9_\-]{1,4}">|</?span>|<span style="display: inline">)'

    junk = re.compile(to_remove, flags=re.M)
    junk = junk.sub('', r.text)
    junk = junk.replace("\n", "")

    proxy_src = re.findall('([0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3})\s*</td>\s*<td>\s*([0-9]{2,6}).{100,1200}(socks4/5|HTTPS?)', junk)
    found = 0
    for src in proxy_src:
        if src[2] == 'socks4/5':
            proto = 'socks5'
        else:
            proto = src[2].lower()
            
        if src:
            proxies.append(proto + '://' +src[0] + ':' + src[1])
            found += 1

    log.debug('Request: %s, found : %s', 'http://proxylist.hidemyass.com/'+page, found)
    """
    list = ''
    for src in proxy_src:
        if src[2] == 'socks4/5':
            proto = 'socks5'
        else:
            proto = src[2].lower()
        if src:
            list += proto + '://' +src[0] + ':' + src[1] + '\n'
    return(list)"""

# ======================================================
# Simple function to do a call to Niantic's system for testing proxy connectivity
def check_proxy(proxy_queue, timeout, proxies):

    # Update check url - Thanks ChipWolf #1282 and #1281
    proxy_test_url = 'https://pgorelease.nianticlabs.com/plfe/rpc'
    proxy = proxy_queue.get()

    if proxy and proxy[1]:

        log.debug('Checking proxy: %s', proxy[1])

        try:
            proxy_response = requests.post(proxy_test_url, '', proxies={'http': proxy[1], 'https': proxy[1]}, timeout=timeout)

            if proxy_response.status_code == 200:
                log.debug('Proxy %s is ok', proxy[1])
                proxy_queue.task_done()
                proxies.append(proxy[1])
                return True

            elif proxy_response.status_code == 403:
                proxy_error = "Proxy " + proxy[1] + " is banned - got status code: " + str(proxy_response.status_code)

            else:
                proxy_error = "Wrong status code - " + str(proxy_response.status_code)

        except requests.ConnectTimeout:
            proxy_error = "Connection timeout (" + str(timeout) + " second(s) ) via proxy " + proxy[1]

        except requests.ConnectionError:
            proxy_error = "Failed to connect to proxy " + proxy[1]

        except Exception as e:
            proxy_error = e

    else:
            proxy_error = "Empty proxy server"

    log.warning('%s', proxy_error)
    proxy_queue.task_done()

    return False

# ======================================================
# Check all proxies and return a working list with proxies
def check_proxies(proxys, proxy_timeout):

    proxy_queue = Queue()
    total_proxies = len(proxys)
           
    proxies = []

    for proxy in enumerate(proxys):
        proxy_queue.put(proxy)

        t = Thread(target=check_proxy,
                   name='check_proxy',
                   args=(proxy_queue, proxy_timeout, proxies))
        t.daemon = True
        t.start()

    # This is painfull but we need to wait here untill proxy_queue is completed so we have a working list of proxies
    proxy_queue.join()

    working_proxies = len(proxies)

    if working_proxies == 0:
        log.error('Proxy was configured but no working proxies was found! We are aborting!')
        sys.exit(1)
    else:
        log.info('Proxy check completed with %d working proxies of %d configured', working_proxies, total_proxies)
        return proxies

# ======================================================
"""
f = open('myfile','w')
f.write('hi there\n') # python will convert \n to os.linesep
f.close() # you can omit in most cases as the destructor will call it
"""
if __name__ == "__main__":
    p = configargparse.ArgParser()
    p.add_argument('-cf', '--config-file', is_config_file=True, help='config file path')
    p.add_argument('-p', '--pages', help='Number of pages to scrape',type=int, default=1)
    p.add_argument('-pt', '--proxy-timeout', help='Timeout settings for proxy checker in seconds', type=int, default=5)
    p.add_argument('-f', '--file', help='Output file, default print in console')
    p.add_argument(
        '-fl',
        '--flat',
        help='Flat format like http://ip;port\n ( default :[http://ip;port, ...])',
        action='store_true',
        default=False
    )
    p.add_argument('-v', help='verbose', action='store_true', default=False)
    p.add_argument('-d', help='debug', action='store_true', default=False)

    args = p.parse_args()
    
    if args.v:
        log.setLevel(logging.INFO)

    if args.d:
        log.setLevel(logging.DEBUG)
    
    
    
    try:
        proxies = scrapes_hma(args.pages)
        working_proxies = check_proxies(proxies, args.proxy_timeout)

        if args.file is None:
            print(working_proxies)
        else:
            f = open(args.file, 'w+')
            if args.flat:
                for wp in working_proxies:
                    f.write(wp + '\n')
            else :
                f.write('[' + ', '.join(working_proxies) + ']')
                
            f.close()

    except Exception as e:
        log.error('%s', e)
