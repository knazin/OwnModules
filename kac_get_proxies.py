import sys
import lxml.html
import kac_download
from bs4 import BeautifulSoup as bs # tylko aby sprawdzac pobrany html
from kac_mongo import KacMongo

def from_net(url='http://free-proxy-list.net/'):
    try:
        mdb = conn_to_db(nazwabazy='crawl', nazwakolekcji='proxies')

        # za czesto uzywany nie dziala - strona blokuje pobieranie
        # html_of = kac_download.Downloader(delay=1,proxies=None,timeout=10.0)
        # html = html_of('http://free-proxy-list.net/')
        # print(bs(html,"lxml").prettify()) # 

        html = kac_download.phantomjs_download(url)
        # print(bs(html2,"lxml").prettify()) #

        tree = lxml.html.fromstring(html)
        rows = tree.cssselect('tr')
        table_rows = []

        for r in rows:
            if r.cssselect('td') != []:
                tds = r.cssselect('td')
                if tds[3].text_content() != 'Russian Federation' and tds[4].text_content() == 'anonymous' and tds[6].text_content() == 'no':
                    table_rows.append('http://{}:{}'.format(str(tds[0].text_content()),str(tds[1].text_content())))

        for tr in table_rows: mdb.insert(dictObject={"proxy": tr})

        for tr in table_rows: print('Dodano proxy: {}'.format(tr))

        print('x')
    except Exception as e:
        print(str(e))

def from_database():
    """Zwraca liste proxy"""
    mdb = conn_to_db(nazwabazy='crawl', nazwakolekcji='proxies')
    proxies = []

    for i in mdb.find():
        proxies.append(i['proxy'])

    return proxies

def check_proxies(nazwakolekcji='spiders'):
    """Sprawdza czy sa jakies proxy ktore slabo pobieraja / maja timeouty \n
    Dane pobiera z bazy 'wyniki' dla wybranej kolekcji"""

    proxies = from_database()
    mdb = conn_to_db(nazwabazy='wyniki', nazwakolekcji=nazwakolekcji)
    avg_of_prox = {}

    for proxy in proxies:
        naz = 'srednie_czasy_pobierania.{}'.format(proxy.replace('.',','))
        x = mdb.find(dictmatch={naz: {"$gt": 6}})
        if x != []: delete_bad_proxy(proxy)

    if len(proxies) < 10:
        from_net()

def delete_bad_proxy(proxy,nazwakolekcji='proxies'):
    """
    usuwa slabe proxy - jesli jest ich za malo pobiera nowe
    proxy - adres url serwera proxy
    """
    mdb = conn_to_db(nazwabazy='crawl', nazwakolekcji=nazwakolekcji)
    ile = mdb.delete(dictmatch={"proxy": proxy})

    lista_proxy =  mdb.find()
    if lista_proxy == []:
        from_net()
    elif len(lista_proxy) < 10:
        from_net()
    else: pass

def conn_to_db(nazwabazy='test',nazwakolekcji='test', nowakolekcja=False):
    mongodb = KacMongo()
    mongodb.get_database(nazwabazy) # 'queue'
    if nowakolekcja:
        mongodb.drop_collection(nazwakolekcji) # 'spider'
    mongodb.get_collection(nazwakolekcji=nazwakolekcji) # 'spider'

    return mongodb

if __name__ == "__main__":
    # delete_bad_proxy('asd')
    # get_proxies_from_net('https://free-proxy-list.net/')
    # from_database()
    check_proxies()

    print('Trzymaj program')

    sys.exit()