from collections import defaultdict

def index(terms, files):  #terms - массив слов, files - массив имён файлов
    d = defaultdict(list)  #Создаем словарь
    for term in terms:  #Смотрим на каждое слово
        for elem in files:   #            Открываем каждый текстовый файл и
            text = open(elem, 'r').read() #   смотрим есть ли там наше слово
            if term in text:
                d[elem[-5]].append(term)   #Если есть добавляем его в словарь с № документа
    return d
