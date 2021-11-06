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
    url = soup.find('a', attrs={'class': 'enquete-descricao__link'})['href']
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    titulo = soup.find('h1', attrs={'class': 'g-artigo__titulo'})
    print(f'Título: {titulo}')
    return titulo


def get_dados_votacao(url):
    url = 'https://www.camara.leg.br/internet/votacao/' + url
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    #print(f'Pagina voto: {url}')

    proposicao = soup.find('strong').text
    print(f'\nProposição: {proposicao}')

    div = soup.find('div', attrs={'id': 'corpoVotacao'})
    inicio_votacao = div.find(
        "strong", text="Início da votação: ").next_sibling
    print(f'\nInício votação: {inicio_votacao.strip()} ')

    itens = ','.join([''.join([item.previous_sibling, item.text, item.next_sibling])
                      for item in soup.select(".coluna1")])
    infoVotacao = ' '.join(itens.split()).replace(",", "\n")
    print(f'\nDados Votacao:\n {infoVotacao} ')

    listaVotacao = soup.find('div', attrs={'id': 'listagem'})
    table = listaVotacao.find('table', attrs={'class': 'tabela-2'})
    table_body = table.find('tbody')
    rows = table_body.find_all('tr')
    voto = ""
    lista_voto = ""
    for row in rows:
        if row.find('th') != None:
            estado = row.text.strip()
        else:
            for td in row.find_all('td'):
                voto = voto + " " + td.text.strip()
            lista_voto = lista_voto + " " + estado + " " + voto + "\n"
        voto = ""

    print(f'\nVotos: {lista_voto}')


def post_page():
    base_url = 'https://www.camara.leg.br/internet/votacao/default.asp'

    post_data = {'OutroMes': '01/11/2021'}
    page = requests.post(base_url, data=post_data)
    soup = BeautifulSoup(page.content, 'html.parser')
    lis = soup.find_all('li', attrs={'class': None})
    pegou_proposta = False

    for li in lis:
        if li.find('a') != None:
            url = li.find('a')['href']
            text = li.find('a').text.strip()

            if text.startswith('PL') or text.startswith('PEC') or text.startswith('PLP'):
                if get_page(url) != None:
                    print('\n-----' * 10)
                    print(f'Pagina proposicao: {url}')
                    pegou_proposta = True

            if pegou_proposta and text.startswith('Relação de votantes por UF'):
                pegou_proposta = False
                get_dados_votacao(url)


post_page()
