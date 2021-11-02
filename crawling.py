import requests
from bs4 import BeautifulSoup

def get_page(url):
    url = 'https:' + url
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    iframe_url = soup.find('iframe')['src']
    page = requests.get(iframe_url)
    soup = BeautifulSoup(page.content, 'html.parser')
    url = 'https://forms.camara.leg.br/' + soup.find('a')['href']
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    result = soup.find('a', attrs={'class':'enquete-descricao__link'})['href']
    print(result)

def post_page():
    base_url = 'https://www.camara.leg.br/internet/votacao/default.asp'

    post_data = {'OutroMes': '01/8/2021'}
    page = requests.post(base_url, data = post_data)
    soup = BeautifulSoup(page.content, 'html.parser')
    lis = soup.find_all('li', attrs={'class': None})

    for li in lis:
        if li.find('a') != None:
            url = li.find('a')['href']
            text = li.find('a').text.strip()

            if text.startswith('PL') or text.startswith('PEC') or text.startswith('PLP'):
                print(text, url)

get_page('//www.camara.leg.br/internet/sileg/prop_lista.asp?sigla=PL&Numero=2633&Ano=2020')
