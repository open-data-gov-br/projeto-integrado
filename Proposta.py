from typing import List
from VotoDeputado import VotoDeputado
from IndicacaoVotoPartido import IndicacaoVotoPartido


class Proposta:
    def __init__(self, id_proposta, codigo, titulo, sub_titulo, data_hora, paragrafos, quantidade_de_votos_publicos, votos_dos_deputados, indicacao_de_votos_dos_partidos, url):
        self.id_proposta = id_proposta
        self.codigo = codigo
        self.titulo = titulo.strip().replace('\n', '')
        self.sub_titulo = sub_titulo.strip().replace('\n', '')
        self.data_hora = data_hora.strip()
        self.paragrafos = paragrafos.strip().replace('\n', '')
        self.quantidade_de_votos_publicos = quantidade_de_votos_publicos
        self.votos_dos_deputados: List[VotoDeputado] = votos_dos_deputados
        self.indicacao_de_votos_dos_partidos: List[IndicacaoVotoPartido] = indicacao_de_votos_dos_partidos
        self.url = url
