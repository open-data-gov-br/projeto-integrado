import requests
from bs4 import BeautifulSoup

base_url = "https://www.camara.leg.br/internet/votacaoDBF/pages/ListaVotacao5603.asp"
url = 'https://www.camara.leg.br/internet/'

page = requests.get(base_url)
soup = BeautifulSoup(page.content, 'html.parser')
trs = soup.find_all('tr', class_=['even', 'odd'])

for tr in trs:
    full_url = url + tr.find('a').attrs['href'].replace('../../', '')
    data = requests.get(full_url)

    file_name = full_url.split('/')[-1]
    print(file_name)
    with open('files/' + file_name, 'wb') as file:
        file.write(data.content)