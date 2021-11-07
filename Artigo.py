class Artigo:
    def __init__(self, titulo, sub_titulo, data_hora, paragrafos, quantidade_de_votos_publicos):
        self.titulo = titulo.strip().replace('\n','')
        self.sub_titulo = sub_titulo.strip().replace('\n','')
        self.data_hora = data_hora.strip()
        self.paragrafos = paragrafos.strip().replace('\n', '')
        self.quantidade_de_votos_publicos = quantidade_de_votos_publicos

    def __str__(self):
        return f'''Titulo: {self.titulo} \nSub-titulo: {self.sub_titulo} \nData e hora: {self.data_hora} \nParagrafos: {self.paragrafos} \n
                   Quantidade de votos: {self.quantidade_de_votos_publicos} \n'''