pogomap_hma_proxy_scraper
=================

Hyde My Ass proxy scraper and checker for Pokemon Go Niantic API.
Can output a proxy list to past into the config file at <i>--proxy</i> argument for [PokemonGoMap/PokemonGo-Map](https://github.com/PokemonGoMap/PokemonGo-Map/blob/develop/pogom/proxy.py).

Requirements:
```
requests, print_function, configargparse, re
```

Usage is as follows:
```
usage: pgm_hma_proxy.py [-h] [-cf CONFIG_FILE] [-p PAGES] [-pt PROXY_TIMEOUT] [-f FILE] [-fl] [-v] [-d]

Args that start with '--' (eg. -p) can also be set in a config file (specified
via -cf).

optional arguments:
  -h, --help            show this help message and exit
  -cf CONFIG_FILE, --config-file CONFIG_FILE
                        config file path
  -p PAGES, --pages PAGES
                        Number of pages to scrape
  -pt PROXY_TIMEOUT, --proxy-timeout PROXY_TIMEOUT
                        Timeout settings for proxy checker in seconds
  -f FILE, --file FILE  Output file, default print in console
  -fl, --flat           Flat format like http://ip;port ( default
                        :[http://ip;port, ...])
  -v                    verbose
  -d                    debug
```

Output with -fl, --flat option :
```
socks5://202.228.236.230:3118
http://222.82.37.294:80
https://193.233.102.6:3118
socks5://187.217.228.58:80
http://201.206.56.278:3118
https://62.55.242.70:8080
http://224.62.225.9:80
```
Output without -fl, --flat option :
```
[socks5://202.228.236.230:3118, http://222.82.37.294:80, https://193.233.102.6:3118, socks5://187.217.228.58:80, http://201.206.56.278:3118, https://62.55.242.70:8080, http://224.62.225.9:80]
```

Based from:
 * [sdrobs/HMA-Proxy-Scraper](https://github.com/sdrobs/HMA-Proxy-Scraper)
 * [PokemonGoMap/PokemonGo-Map/pogom/proxy.py](https://github.com/PokemonGoMap/PokemonGo-Map/blob/develop/pogom/proxy.py)
