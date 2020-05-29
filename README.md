# HydraRecon
Simple recon tool 

# Features

- subdoamin enumeration
- check live domains
- simple port scanner
- take screenshot for domains
- crawler:
  * parse js files 
  * parse robots.txt
  * parse sitemap.xml
  * collect archived urls
  
 # installation
```
git clone https://github.com/aufzayed/HydraRecon.git

pip3 install -r requirements.txt
```
  
 ```
                __           
|__|   _| _ _ |__)_ _ _  _  
|  |\/(_|| (_|| \(-(_(_)| ) 
    /                       


usage: 

hydrarecon Methods:
	1.basic :: 
		- subdomain enumeration
		- scan common ports
		- screenshot hosts
		- html report
	2.crawl :: 
		- sitemap.xml
		- robots.txt
		- related urls: 
			* wayback machine
			* virus total
			* common crawl
			* urlscan

	3.config :: config hydra

examples:
	python3 hydrarecon.py --basic -d example.com
	python3 hydrarecon.py --crawl -d example.com
	python3 hydrarecon.py --config

optional arguments:
  -h, --help       show this help message and exit
  --basic          use basic recon module
  --crawl          use crawl module
  --config         initializing config file
  -d , --domain    domain to crawl or recon
  -p , --ports     ports to scan: (small | large | xlarge). default: small
  -T , --timeout   control http request timeout in seconds, default: 1s
  -t , --threads   number of threads, default: 10
  -o , --out       path to save report, default : home directory

 ```
 
 ### Examples:
 ```
 python3 hydrarecon.py --basic -d example.com = python3 hydrarecon.py --basic -d example.com -t 10 -T 1 -o ~ -p small
 python3 hydrarecon.py --crawl -d example.com = python3 hydrarecon.py --crawl -d example.com -t 10 -o ~
 ```
 ### Notes
- if you have virustoal API key use ```python3 hydrarecon.py --config``` (optional)
- ```--crawl``` option results depends on ```--basic``` results
# Thanks
### this tool inspired by:
- httprobe, waybackurls by [@tomnomnom](https://github.com/tomnomnom)
- hakrawler by [@hakluke](https://github.com/hakluke)
- aquatone by [@michenriksen](https://github.com/michenriksen)
- LinkFinder by [@GerbenJavado](https://github.com/GerbenJavado)
- subjs by [@lc](https://github.com/lc)
