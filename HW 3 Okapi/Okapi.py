from collections import defaultdict, Counter
from pymystem3 import Mystem
from nltk.corpus import stopwords
from math import log
import os
import re

def main_func():
    all_lemmas = {}
    article_data = {}
    avdl = 0
    
    for article in os.listdir('./articles'):
        textwithtags = open('./articles/'+article,'r',encoding='utf-8-sig').read()
        url = re.findall('@url (.*)', textwithtags)[0]
        name = re.findall('@ti (.*)', textwithtags)[0]
        text = re.findall('article=[0-9]+(.*)', textwithtags, flags= re.DOTALL)
        m = Mystem()
        if len(text) > 0:
            text = text[0]
            text = re.sub('[&!?*&@#/.,:.,"––)(«»№]', '', text)
            words = [i.lower() for i in text.split()]

            lemmas = []
            for word in words:
                if word not in stopwords.words('russian'):
                    lll = m.lemmatize(word)
                    lemmas.append(lll[0])
                    
            all_lemmas[article] = lemmas
            article_data[article] = (url, name, len(lemmas))
            avdl += len(lemmas)

    avdl = avdl / len(all_lemmas)
    inverted_index = invert_index(all_lemmas)
    return article_data, avdl, inverted_index
    
def invert_index(all_lemmas):
    d = defaultdict(list)
    for w, art in all_lemmas.items():
        article_count = Counter(art)
        for word,freq in article_count.items():
            d[word].append((w,freq))
    return d

def score_BM25(n, qf, N, dl, avdl):
    k1 = 2.0
    b = 0.75
    K = compute_K(dl, avdl, k1, b)
    IDF = log((N - n + 0.5) / (n + 0.5))
    frac = ((k1 + 1) * qf) / (K + qf)
    return IDF * frac


def compute_K(dl, avdl, k1, b):
    return k1 * ((1-b) + b * (float(dl)/float(avdl)))

def search(request):
    appropriate = defaultdict(float)
    m = Mystem()
    article_data, avdl, inverted_index = main_func()
    N = len(article_data)
    text = re.sub('[&!?*&@#/.,:.,"––)(«»№]', '', request)
    words = [i.lower() for i in text.split()]

    lemmas = []
    for word in words:
        if word not in stopwords.words('russian'):
            lll = m.lemmatize(word)
            lemmas.append(lll[0])

    for lemma in lemmas:
        if lemma in inverted_index:
            lemma_count = inverted_index[lemma]
            n = len(lemma_count)
            for l in lemma_count:
                data = article_data[l[0]]
                qf = l[1]
                dl = data[2]
                appropriate[(data[0],data[1])] += score_BM25(n, qf, N, dl, avdl)
                
    result = sorted(appropriate)
    return result

result = search('каникулы на новый год и рождество')

for i in result[:10]:          #Тут надо было Display, но у меня проблемы с Анакондой((
    print(i)

