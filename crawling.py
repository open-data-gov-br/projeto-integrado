import requests
from bs4 import BeautifulSoup

def get_page():
    base_url = 'https://www2.camara.leg.br/atividade-legislativa/plenario/resultadoVotacao'

    page = requests.get(base_url)
    soup = BeautifulSoup(page.content, 'html.parser')
    lis = soup.find_all('li', attrs={'class': None})

    for li in lis:
        print(li)

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

post_page()
