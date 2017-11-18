import os # mozna usunac
import time
import socket
import random
import urllib
import urllib3
import certifi # aby ssl dzialalo
import kac_get_proxies
from selenium import webdriver
from bs4 import BeautifulSoup as bs # tylko aby sprawdzac pobrany html
from urllib.parse import urlparse #import urlparse
# from sleep import Throttle

DEFAULT_AGENT = 'wswp'
DEFAULT_DELAY = 1
DEFAULT_RETRIES = 1
DEFAULT_TIMEOUT = 3
DEFAULT_PROXIES = 1

class Downloader:
    """Zwraca html \n
    Domyslnie pobiera proxy z wlasnej listy/bazy - chyba ze podasz mu wlasna"""

    def __init__(self, delay=DEFAULT_DELAY, user_agent=DEFAULT_AGENT, proxies=DEFAULT_PROXIES, num_retries=DEFAULT_RETRIES, timeout=DEFAULT_TIMEOUT):
        socket.setdefaulttimeout(timeout)
        self.throttle = 1 # Throttle(delay)
        self.user_agent = user_agent
        if proxies == 1: self.proxies = kac_get_proxies.from_database()
        else: self.proxies = proxies
        self.proxy = ''
        self.num_retries = num_retries
        self.timeout = timeout


    def __call__(self, url):
        result = None           
            
        try: 
            with open('user-agents.txt','r') as f:
                self.user_agent = random.choice(f.readlines())[:-2]
        except Exception as e: pass

        # self.throttle.wait(url) # odczekaj x sekund

        try: self.proxy = random.choice(kac_get_proxies.from_database())           
        except Exception as e: self.proxy = None
        if self.proxies == None: self.proxy = None

        headers = {'User-agent': self.user_agent}
        result = Downloader.download(url, headers, self.proxy, self.num_retries, self.timeout)

        # print(bs(result).prettify()) # 

        return result


    def download(url3, headers, proxy, num_retries, timeout):
        """Pobierz zawartosc strony
        url - adres strony internetowej 
        header - podaj tablice z danymi komputera (przegladarka, system operacyjny itp) (accept None)
        proxy - podaj adres serwera proxy (accept None)
        num_retires - ile razy probowac pobrac strone
        """

        if proxy:
            https = urllib3.ProxyManager(
                proxy_url= proxy,
                num_pools=10,
                headers=headers,
                proxy_headers=headers,
                cert_reqs='CERT_REQUIRED', 
                ca_certs=certifi.where(),
                timeout= urllib3.util.Timeout(connect=2.0,read=timeout), #read=3.0
            )
        else: 
            https = urllib3.PoolManager( 
                headers=headers, 
                cert_reqs='CERT_REQUIRED', 
                ca_certs=certifi.where(), 
                timeout= urllib3.util.Timeout(connect=2.0,read=timeout), #read=3.0
                )
        
        try: html = https.urlopen('GET',url3).data.decode('utf-8')
        except Exception as e: 
            html = ''

        return html

    def get_proxy(self):
        return self.proxy

def phantomjs_download(url):
    b = webdriver.PhantomJS(executable_path="/Applications/phantomjs-2.1.1-macosx/bin/phantomjs")
    b.get(url)
    html2 = b.page_source

    return html2

def firefox_download(url):
    browser = webdriver.Firefox(executable_path="/Library/Frameworks/Python.framework/Versions/3.6/lib/python3.6/site-packages/selenium/webdriver/firefox/geckodriver") # "/Library/Frameworks/Python.framework/Versions/3.6/lib/python3.6/site-packages/selenium/webdriver/firefox/geckodriver"
    browser.get(url)

    html = browser.page_source
