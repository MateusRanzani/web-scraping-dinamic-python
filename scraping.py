import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
import math

url = 'https://www.kabum.com.br/espaco-gamer/cadeiras-gamer'

headers = {'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 \
    (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"}

site = requests.get(url, headers=headers)
soup = BeautifulSoup(site.content, 'html.parser')
qtd_itens = soup.find('div', id='listingCount').get_text().strip()
index = qtd_itens.find(' ')
qtd = qtd_itens[:index]

ultima_pagina = math.ceil(int(qtd)/ 20)
dic_produtos = { 'marca':[], 'preco':[] }

for i in range(1, ultima_pagina+1):
    url_pag = f'https://www.kabum.com.br/espaco-gamer/cadeiras-gamer?page_number={i}&page_size=20&facet_filters=&sort=most_searched'
    site = requests.get(url_pag, headers=headers)
    soup = BeautifulSoup(site.content, 'html.parser')
    produtos = soup.find_all('div', class_= re.compile('productCard'))

    for produto in produtos:
        marca = produto.find('span', class_=re.compile('nameCard')).get_text().strip()
        preco = produto.find('span', class_=re.compile('nameCard')).get_text().strip()

        dic_produtos['marca'].append(marca)
        dic_produtos['preco'].append(preco)

df = pd.DataFrame(dic_produtos)
df.to_csv('/home/mateus/Transferências', encoding='utf-8', sep=";")
