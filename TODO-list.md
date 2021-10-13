# TODO-list

## Visão geral
Extrair as leis, titulo, sub-titulo e primeiro paragrafo, depois tratar os resultados e agrupar por deputado e partido.
Criar um web app pra o usuário colocar email e simular votação nos projetos de leis, no final o aplicativo vai exibir qual partido e deputado o usário tem mais afinidade.

# TODO
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