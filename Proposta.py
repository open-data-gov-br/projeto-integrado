from typing import List
from Voto import Voto

class Proposta:
    def __init__(self, id, codigo, titulo, sub_titulo, data_hora, paragrafos, quantidade_de_votos_publicos, votacao):
        self.id = id
        self.codigo = codigo
        self.titulo = titulo.strip().replace('\n','')
        self.sub_titulo = sub_titulo.strip().replace('\n','')
        self.data_hora = data_hora.strip()
        self.paragrafos = paragrafos.strip().replace('\n', '')
        self.quantidade_de_votos_publicos = quantidade_de_votos_publicos
        self.votacao:List[Voto] = votacao