pogomap_hma_proxy_scraper
=================

A proxy scraper in Node.js

Installation:
```
$ pip install -r requirements.txt
```

Usage is as follows:
```
	python ./pgm_hma_proxy.py 10 10 format
```

Output is in the form of proto://ip:port
```
{ 
  '202.228.236.230' : '3118',
  '222.82.37.294'   : '80',
  '193.233.102.6'   : '3118',
  '187.217.228.58'  : '80',
  '201.206.56.278'  : '3118',
  '62.55.242.70'    : '8080',
  '224.62.225.9'    : '80',
  ...etc
}
```

Based from: [sdrobs/HMA-Proxy-Scraper](https://github.com/sdrobs/HMA-Proxy-Scraper)
Based from: [PokemonGoMap/PokemonGo-Map/pogom/proxy.py](https://github.com/PokemonGoMap/PokemonGo-Map/blob/develop/pogom/proxy.py)
