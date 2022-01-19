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
    df = df.sort_values(by='votos_publicos', ascending=False)
    df = df.head(5)
    return json.dumps(json.loads(df.to_json(orient="records")))

if __name__ == '__main__':
    app.run()