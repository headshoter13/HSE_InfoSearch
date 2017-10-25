from bs4 import BeautifulSoup
import requests

def main_func(page):
    n = 2000
    while n < 3000:
        url = page + str(n)
        HTML = requests.get(url)

        author, name, date, topic, text = retrieve_info(HTML)
        write_data(author, name, date, topic, url, text)
        n += 1

def retrieve_info(HTML):
    soup = BeautifulSoup(HTML.text,'lxml')

    author = soup.find('div',class_='author')
    if author is None:
        author = 'Noname'
    else:
        author = author.text.strip()
    name = soup.find('div', class_='title').text.strip()
    date = soup.find('div',class_='clock').text.strip()
    topic = soup.find('div',class_='razdel').text.strip()

    texts = soup.findAll('p',class_='MsoNormal')
    text = '\n\n'.join([i.text.strip() for i in texts])

    return(author, name, date, topic, text)


def write_data(author, name, date, topic, url, text):
    name1 = name.strip('?!.,#@$%^&*')
    with open('./articles1/'+str(name1)+'.txt','w',encoding='utf-8-sig') as f:
        f.write('@au ' + str(author) + '\n@ti ' + str(name) + '\n@da ' + str(date) + '\n@topic ' + str(topic) + '\n@url ' + str(url) + '\n' + str(text))
    
 

main_func('http://www.istoki-rb.ru/index.php?article=')
