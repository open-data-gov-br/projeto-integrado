import joblib
import os 

from flask import Flask, request, render_template
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired
import numpy as np
import pandas as pd
import json

app = Flask(__name__)
app.config['SECRET_KEY']='wP4xQ8hUljJ5oI1c'
bootstrap = Bootstrap(app)

class InputForm(FlaskForm):
    uf = StringField('UF:', validators=[DataRequired()])

@app.route('/', methods=['GET', 'POST'])
def index():
    form   = InputForm(request.form)
    name = 'No-name'
    if form.validate_on_submit():
        print(form.uf.data)
    
    return render_template('index.html', form=form, name=name)

@app.route('/hello', methods=['GET'])
def get_propostas():
    df = pd.read_csv('propostas.csv', sep=',')
    df = df.groupby('id_proposta').first()
    df = df.reset_index()
    df = df.sort_values(by='votos_publicos', ascending=False)
    df = df.head(10)
    return json.dumps(json.loads(df.to_json(orient="records")))

@app.route('/resultado', methods=['POST'])
def calcula_resultado():
    respostas = request.json

    listaDeDeputados = []
    listaDePartidos = []

    df_propostas = pd.read_csv('propostas.csv', sep=',')
    df_deputados = pd.read_csv('votosDeputados.csv', sep=',')
    df_partidos = pd.read_csv('IndicacaoVotoPartido.csv', sep=',')

    # Deputados

    df_deputados = df_deputados[df_deputados['uf'] == 'São Paulo (SP)']

    for reposta in respostas:

        proposta = df_propostas[df_propostas['id_proposta'] == reposta['id_proposta']].head(1)
        titulo_da_proposta = proposta['titulo'].item()
        codigo_da_proposta = proposta['codigo'].item()
        deputados_pela_proposta = df_deputados[df_deputados['id_proposta'] == reposta['id_proposta']]

        for index, row in deputados_pela_proposta.iterrows():
            if row["voto"] == reposta['voto'] and int(proposta['data_hora']) == int(row['data_hora']):
                deputado_existe = verifica_se_deputado_ja_existe(row["nome_do_deputado"], listaDeDeputados)
                
                if deputado_existe:
                    for deputado in listaDeDeputados:
                        if deputado["nome_do_deputado"] == row["nome_do_deputado"]:
                            deputado['pontuacao'] = deputado['pontuacao'] + 1
                            deputado['propostas'].append({
                                'id_proposta' : int(proposta['id_proposta']),
                                'codigo': codigo_da_proposta,
                                'titulo' : titulo_da_proposta,
                                'voto': reposta['voto']
                            })
                else:
                    listaDeDeputados.append({
                        'nome_do_deputado' : str(row['nome_do_deputado']),
                        'nome_do_partido': str(row['nome_do_partido']),
                        'propostas': [{
                            'id_proposta' : int(proposta['id_proposta']),
                            'codigo' : codigo_da_proposta,
                            'titulo' : titulo_da_proposta,
                            'voto': reposta['voto']
                        }],
                        'pontuacao' : 1
                    })
        
        deputados_pela_proposta = None

    listaDeDeputados.sort(key=lambda x: x['pontuacao'], reverse=True)

    # Partidos

    for reposta in respostas:

        proposta = df_propostas[df_propostas['id_proposta'] == reposta['id_proposta']].head(1)
        titulo_da_proposta = proposta['titulo'].item()
        codigo_da_proposta = proposta['codigo'].item()
        partidos_pela_proposta = df_partidos[df_partidos['id_proposta'] == reposta['id_proposta']]

        for index, row in partidos_pela_proposta.iterrows():
            if row["voto"] == reposta['voto'] and int(proposta['data_hora']) == int(row['data_hora']):
                partido_existe = verifica_se_partido_ja_existe(row["nome_do_partido"], listaDePartidos)
                
                if partido_existe:
                    for partido in listaDePartidos:
                        if partido["nome_do_partido"] == row["nome_do_partido"]:
                            partido['pontuacao'] = partido['pontuacao'] + 1
                            partido['propostas'].append({
                                'id_proposta' : int(proposta['id_proposta']),
                                'codigo': codigo_da_proposta,
                                'titulo' : titulo_da_proposta,
                                'voto': reposta['voto']
                            })
                else:
                    listaDePartidos.append({
                        'nome_do_partido' : str(row['nome_do_partido']),
                        'propostas': [{
                            'id_proposta' : int(proposta['id_proposta']),
                            'codigo' : codigo_da_proposta,
                            'titulo' : titulo_da_proposta,
                            'voto': reposta['voto']
                        }],
                        'pontuacao' : 1
                    })
        
        partidos_pela_proposta = None

    listaDePartidos.sort(key=lambda x: x['pontuacao'], reverse=True)

    return json.dumps(
        { 
        'deputados' : listaDeDeputados,
        'partidos': listaDePartidos
        }
    )
                

def verifica_se_deputado_ja_existe(nome_do_deputado, listaDeDeputados):
    for deputado in listaDeDeputados:
        if deputado['nome_do_deputado'] == nome_do_deputado:
            return True

    return False

def verifica_se_partido_ja_existe(nome_do_partido, listaDePartidos):
    for partido in listaDePartidos:
        if partido['nome_do_partido'] == nome_do_partido:
            return True

    return False


if __name__ == '__main__':
    app.run()