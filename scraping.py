from datetime import datetime
import requests
from bs4 import BeautifulSoup
import pandas as pd

texto_string = requests.get('https://globoesporte.globo.com/').text
hora_extracao = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

bsp_texto = BeautifulSoup(texto_string, 'html.parser')
lista_noticias = bsp_texto.find_all('div', attrs={'class':'feed-post-body'})
print("Quantidade de manchetes = ", len(lista_noticias))

dados = []

for i, noticia in enumerate(lista_noticias, start=1):
    manchete = noticia.contents[1].text.replace('"', "")
    link = noticia.find('a').get('href')

    descricao = noticia.contents[2].text
    if not descricao:
        descricao = noticia.find('div', attrs={'class': 'bstn-related'})
        descricao = descricao.text if descricao else None

    metadados = noticia.find('div', attrs={'class':'feed-post-metadata'})
    time_delta = metadados.find('span', attrs={'class': 'feed-post-datetime'})
    secao = metadados.find('span', attrs={'class': 'feed-post-metadata-section'})

    time_delta = time_delta.text if time_delta else None
    secao = secao.text if secao else None

    dados.append((manchete, descricao, link, secao, hora_extracao, time_delta))

    print(f"\n### Manchete {i} ###")
    print(f"Manchete: {manchete}")
    print(f"Link: {link}")
    print(f"Descrição: {descricao}")
    print(f"Seção: {secao}")
    print(f"Tempo da postagem: {time_delta}")

df = pd.DataFrame(dados, columns=['manchete', 'descrição', 'link', 'seção', 'hora_extração', 'time_delta'])
df.head()
