import requests
from bs4 import BeautifulSoup
from Proposta import Proposta
import csv
from typing import List
from VotoDeputado import VotoDeputado
from IndicacaoVotoPartido import IndicacaoVotoPartido
import os.path
import datetime

def get_proposta(url) -> Proposta:
    proposta: Proposta = Proposta('', '', '', '', '', '', '', '', '', '')

    url = 'https:' + url
    page = requests.get(url)    
    if (page.status_code != 200):
        #print(f"page.status_code 0 :{page.status_code}")
        return None
    soup = BeautifulSoup(page.content, 'html.parser')

    # Bloco "O QUE VOCÊ ACHA DISSO?"
    iframe_url = soup.find('iframe')['src']
    page = requests.get(iframe_url)    
    if (page.status_code != 200):
        #print(f"page.status_code 1 :{page.status_code}")
        return None
    soup = BeautifulSoup(page.content, 'html.parser')

    # Pagina da enquete
    url = 'https://forms.camara.leg.br' + soup.find('a')['href']
    page = requests.get(url)
    if (page.status_code != 200):        
        return None
    soup = BeautifulSoup(page.content, 'html.parser')

    # Link veja os resultados
    url = soup.find_all(
        'a', attrs={'class': 'link-com-icone-esquerda'})[1]['href']
    url_da_enquete = 'https://forms.camara.leg.br' + url

    page = requests.get(url_da_enquete)
    if (page.status_code != 200):
        print(url_da_enquete)
        return None    
    soup_da_enquete = BeautifulSoup(page.content, 'html.parser')

    quantidade_de_respostas = soup_da_enquete.find_all(
        'td', attrs={'class': 'grafico-barras__item resumo-resposta__participacoes'})
    quantidade_total_de_respostas = 0

    for quantidade_de_resposta in quantidade_de_respostas:
        quantidade_total_de_respostas += int(
            quantidade_de_resposta.text.replace('.', '').strip())

    proposta.quantidade_de_votos_publicos = quantidade_total_de_respostas
    # print('Total de votos: ', proposta.quantidade_de_votos_publicos)

    # Link entenda a proposta
    url = soup.find('a', attrs={'class': 'enquete-descricao__link'})['href']
    proposta.url = url
    page = requests.get(url)    
    if (page.status_code != 200):        
        return None        
    soup = BeautifulSoup(page.content, 'html.parser')

    if soup != None:
        return extrai_dados_da_proposta(soup, proposta)

    return None


def extrai_dados_da_proposta(soup, proposta: Proposta) -> Proposta:
    artigo_titulo = soup.find('h1', attrs={'class': 'g-artigo__titulo'})
    if (artigo_titulo == None):
        return None

    proposta.titulo = artigo_titulo.text

    sub_titulo_element = soup.find('p', attrs={'class': 'g-artigo__descricao'})
    if sub_titulo_element != None:
        proposta.sub_titulo = sub_titulo_element.text
    else:
        proposta.sub_titulo = 'sub-titulo'

    div = soup.find('div', attrs={'class': 'js-article-read-more'})
    paragrafos = div.find_all('p', attrs={'class': None})

    for p in paragrafos:
        proposta.paragrafos += p.text.strip().replace('\n', '')

    return proposta


def get_dados_votacao(url, proposta: Proposta) -> Proposta:
    url = 'https://www.camara.leg.br/internet/votacao/' + url
    page = requests.get(url)
    #print(page)
    if (page.status_code != 200):
        #print(f"page.status_code 5 :{page.status_code}")
        return None
    soup = BeautifulSoup(page.content, 'html.parser')

    div = soup.find('div', attrs={'id': 'corpoVotacao'})
    inicio_votacao = div.find(
        "strong", text="Início da votação: ").next_sibling
    proposta.data_hora = inicio_votacao.strip().replace('\n', '').replace(' ', '').replace('/', '').replace(':', '')

    # Indicacao de voto pelo partido
    listaPartido = soup.find(
        'div', attrs={'class': 'grid-cell size1of2 last-cell'})
    tablePartido = listaPartido.find('table', attrs={'class': 'tabela-2'})
    trsPartido = tablePartido.find_all('tr')
    lista_votosPartido: List[IndicacaoVotoPartido] = list()

    for tr in trsPartido:
        indicacaoPartido: IndicacaoVotoPartido = IndicacaoVotoPartido(
            '', '', '')
        indicacaoPartido.nome_do_partido = tr.find('th').text.strip()[:-1]
        indicacaoPartido.voto = tr.find('td').text.strip()
        lista_votosPartido.append(indicacaoPartido)
    proposta.indicacao_de_votos_dos_partidos = lista_votosPartido

    # Votacao dos Deputados
    listaVotacao = soup.find('div', attrs={'id': 'listagem'})
    table = listaVotacao.find('table', attrs={'class': 'tabela-2'})
    table_body = table.find('tbody')
    trs = table_body.find_all('tr')
    lista_votos: List[VotoDeputado] = list()
    estado = ''

    for tr in trs:
        votoDeputado: VotoDeputado = VotoDeputado('', '', '', '', '')
        if tr.find('th') != None:
            estado = tr.text.strip()
        tds = tr.find_all('td')

        for td in tds:
            if not(td.has_attr('colspan')):
                votoDeputado.nome_do_deputado = tds[0].text.strip()
                votoDeputado.nome_do_partido = tds[1].text.strip()
                votoDeputado.voto = tds[3].text.strip()
                votoDeputado.uf = estado

        if (votoDeputado.nome_do_deputado != '' and
                votoDeputado.nome_do_partido != '' and
                votoDeputado.voto != '' and
                votoDeputado.uf != ''):
            lista_votos.append(votoDeputado)

    proposta.votos_dos_deputados = lista_votos

    return proposta


def post_page():
    base_url = 'https://www.camara.leg.br/internet/votacao/default.asp'
    
    year = int(datetime.datetime.now().date().strftime("%Y"))
    
    for ano in range(year-2,year,1):
        for mes in range(1,13):
            data = '01/' + str(mes) + '/' + str(ano)            
            post_data = {'OutroMes': data}

            page = requests.post(base_url, data=post_data)
            if page.status_code != 200:                
                return
            soup = BeautifulSoup(page.content, 'html.parser')

            lis = soup.find_all('li', attrs={'class': None})
            pegou_proposta = False
            propostas: List[Proposta] = list()

            proposta: Proposta = Proposta('', '', '', '', '', '', '', '', '', '')
            for li in lis:
                if li.find('a') != None:
                    url = li.find('a')['href']
                    text = li.find('a').text.strip()

                    if text.startswith('PL') or text.startswith('PEC') or text.startswith('PLP'):
                        try:
                            proposta = get_proposta(url)
                            if proposta == None:
                                pegou_proposta = False
                            else:
                                proposta.codigo = text
                                pegou_proposta = True
                        except Exception:
                            pegou_proposta = False
                            print(f"Falha ao pegar proposta: {url}")

                    if pegou_proposta and text.startswith('Relação de votantes por UF'):
                        pegou_proposta = False
                        proposta = get_dados_votacao(url, proposta)
                        if proposta != None:
                            proposta.id_proposta = (str(proposta.codigo.split("Nº", 1)[1])).replace('/', '').replace(' ', '').strip()
                            print(proposta.titulo)
                            propostas.append(proposta)

            file_exists = os.path.exists('propostas.csv')
            mode = 'a+' if file_exists else 'w'            
            with open('propostas.csv', mode, encoding='UTF8', newline='') as file:
                writer = csv.writer(file)
                if(mode == 'w'):
                    writer.writerow(['id_proposta', 'codigo', 'data_hora', 'titulo','sub-titulo', 'paragrafos', 'votos_publicos','url'])

                file_exists = os.path.exists('votosDeputados.csv')
                mode = 'a+' if file_exists else 'w'
                with open('votosDeputados.csv', mode, encoding='UTF8', newline='') as fileVotoDeputado:
                    writerVotoDeputado = csv.writer(fileVotoDeputado)
                    if(mode == 'w'):
                        writerVotoDeputado.writerow(['id_proposta', 'data_hora', 'nome_do_deputado','nome_do_partido', 'uf', 'voto'])

                    file_exists = os.path.exists('IndicacaoVotoPartido.csv')
                    mode = 'a+' if file_exists else 'w'
                    with open('IndicacaoVotoPartido.csv', 'a+', encoding='UTF8', newline='') as fileIndicacaoPartido:
                        writerIndicacaoPartido = csv.writer(fileIndicacaoPartido)
                        if(mode == 'w'):
                            writerIndicacaoPartido.writerow(['id_proposta', 'data_hora', 'nome_do_partido', 'voto'])

                        for proposta in propostas:
                            writer.writerow([proposta.id_proposta, proposta.codigo, proposta.data_hora, proposta.titulo,proposta.sub_titulo, proposta.paragrafos, proposta.quantidade_de_votos_publicos, proposta.url])

                            for votoDeputado in (proposta.votos_dos_deputados):
                                writerVotoDeputado.writerow([proposta.id_proposta, proposta.data_hora, votoDeputado.nome_do_deputado, votoDeputado.nome_do_partido, votoDeputado.uf, votoDeputado.voto])

                            for indicacaoPartido in (proposta.indicacao_de_votos_dos_partidos):
                                writerIndicacaoPartido.writerow([proposta.id_proposta, proposta.data_hora, indicacaoPartido.nome_do_partido, indicacaoPartido.voto])


post_page()