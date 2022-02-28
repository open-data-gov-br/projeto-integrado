from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.luhn import LuhnSummarizer
from goose3 import Goose
import matplotlib.pyplot as plt

url = 'https://www.camara.leg.br/noticias/741161-projeto-permite-cessao-voluntaria-de-geracao-extra-de-energia-eletrica-para-hospitais-durante-pandemia/'

g = Goose()
artigo = g.extract(url)
texto_original = artigo.cleaned_text
print("\n texto extraido:",texto_original)

parser = PlaintextParser.from_string(texto_original, Tokenizer('portuguese'))

sumarizador = LuhnSummarizer()

resumo = sumarizador(parser.document, 3)
print('-->')
print(resumo)


