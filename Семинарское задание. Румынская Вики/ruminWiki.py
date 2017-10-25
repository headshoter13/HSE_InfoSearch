import requests
from bs4 import BeautifulSoup

URLS = []

def wiki(url):
    links = []
    req = requests.get(url)
    soup = BeautifulSoup(req.text, 'lxml')

    for link in (soup.findAll('a')):#, attrs = {'class':'href'})):
        if link.has_attr('href'):
            if link['href'][0:2] == '/w':
                #print(link['href'])
                link['href'] = url + link['href']
                link = link['href']
                links.append(link)
    #for i in links:
    #print(i)
    
    return links


def all_url(links,URLS):
    x = 0
    for url in links:
        x += 1
        if url not in URLS:
            URLS.append(url)
            urlss = wiki(url)
            #x = 1
            for i in urlss:
                URLS.append(url)
        print(x)
                #x += 1
    
    #return URLS
        

def writing_txt(URLS = URLS, txt = 'txt_links.txt'):
    fout = open(txt, 'w', encoding = 'utf-8')
    URLS = set(URLS)
    for i in URLS:
        fout.write(i + '\n')
    fout.close()

links = wiki('http://mo.wikipedia.org/')
#links = wiki('http://mo.wikipedia.org//w/index.php?title=%D0%A1%D0%BF%D0%B5%D0%BA%D1%82%D0%B0%D0%BA%D1%83%D0%BB&action=edit&redlink=1')
URLS = all_url(links, URLS)
writing_txt()

