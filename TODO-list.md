# TODO-list

## Visão geral
Extrair as leis, titulo, sub-titulo e primeiro paragrafo, depois tratar os resultados e agrupar por deputado e partido.
Criar um web app pra o usuário colocar email e simular votação nos projetos de leis, no final o aplicativo vai exibir qual partido e deputado o usário tem mais afinidade.

# Caso de uso
- Usuario escolhe quantas PL ele quer votar pra decidir
- Usuario vai selecionar qual estado vai analisar (deputado)
- Quanto mais o usuario escolher mais preciso vai ficar
- Pegar os mais populares com base em votos
- Extrair os ultimos 3 meses de dados

- Base
https://www2.camara.leg.br/atividade-legislativa/plenario/resultadoVotacao

- Votação
https://www.camara.leg.br/internet/votacao/mostraVotacao.asp?ideVotacao=10181&numLegislatura=56&codCasa=1&numSessaoLegislativa=3&indTipoSessaoLegislativa=O&numSessao=117&indTipoSessao=E&tipo=uf
(Orientação do partido, nome, UF, partido, voto S/N)

- Proposição -> Pagina da LP -> O QUE VOCÊ ACHA DISSO? (RESPONDA) -> Veja os resultados
https://forms.camara.leg.br/ex/enquetes/2252939/resultado
(Ler a quantidade de votos que a LP teve e somar - campo popularidade da PL)

- Entenda a proposta 
https://www.camara.leg.br/noticias/665270-projeto-permite-que-radio-comunitaria-com-operacao-suspensa-volte-a-funcionar-devido-a-pandemia/
(Titulo, sub-titulo e 3 primeiros paragrafos) - Adicionar link para saber mais sobre

## TODO
### Sprint 1
- Escrever o artigo
    1. Introdução
    2. Contextualização
    3. Problema Proposto
    4. Coleta de Dados
- Analise dos arquivos (.txt) tabulados com os votos, fazer a leitura com Python
- Extrair os dados das paginas (4 páginas - web scraping)
 - Ler os votos e os deputados de cada PL se o plano de ler os .txts não der certo
 - Ler a quantidade de votos publicos em cada PL (pegar do grafico)
 - Ler o "entenda a proposta" (Titulo, sub-titulo e 3 primeiros paragrafos)

 Tabela PL_PLP_PEC (id, titulo, sub-titulo, paragrafos, quantidade_de_votos_publicos, data_de_criacao)

 data_de_criacao -> 

### Sprint 2
- Escrever o artigo

     5. Processamento e Tratamento de Dados   
     6. Análise Exploratória dos Dados e Análise com Ciência de Dado   
     7. Discussão dos Resultados   
     8. Links   
     9. Conclusão    
     10. Referências	   

- Tratar os dados e guardar em arquivos .csv
 - endpoint que pega um numero X de propostas e devolve uma estrutura JSON pro front-end
 - montar a tela das perguntas e guardar as respostas (1, 0, 0, 1)
 - pega a votacao de uma proposta por Id (votosDeputados.csv filtrar uf e proposta_id) (IndicacaoVotoPartido.csv filtrar uf e proposta_id) 
 ordenar pelo top X e invertido para os dois casos, deputados e partido, calculo de porcentagem
 - endpoint que envia as respostas e devolve a lista de deputados e partidos em JSON
 - criar uma tela pra exibir os resultados

- Web app de um quiz básico que le de um arquivo .csv as perguntas e guarda as respostas
- Algoritmo para coeficiente de correlacao [aula 04](https://github.com/andredarcie/my-data-science-notebooks/blob/master/estatistica-e-aplicacoes/aula04_pratica.ipynb)
- Deploy no Heroku da aplicação web

20/11/2021 - Versao preliminar
29/01/2022 - Relatorio tecnico
05/02/2022 - Defesa

