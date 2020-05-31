import os
from flask import Flask, jsonify, request, render_template, Response, send_file, stream_with_context, make_response
import json
import numpy as np
import pandas as pd
from flask_cors import CORS, cross_origin

app = Flask(__name__)

cors = CORS(app, resources={r"/api/*": {"origins": "*"}}, support_credentials=True)
app.config['CORS_HEADERS'] = 'Content-Type'

from sklearn import preprocessing
from sklearn.linear_model import LinearRegression

#Vars de controle
path = 'final.csv'
drop = [0, 1, 5, 6, 7, 8, 9, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 22, 23, 24, 25, 26, 27, 28, 30, 31]
prever = [0, 1, -1] #Indices do novo DF!!

#Vars globais
normalizer = -1
df = pd.DataFrame()
lm = -1

def inialize():
    global df
    global prever
    global path
    global normalizer
    global drop
    global lm

    #Lendo
    df = pd.read_csv(path)

    #Arrumando colunas
    df.drop(df.columns[drop], axis=1, inplace=True)

    df_cases = df.iloc[:, 2]
    df.drop('Cases_per_mil', axis=1, inplace=True)

    cs = df.columns

    #Normalizando
    normalizer = preprocessing.Normalizer().fit(df)
    df = normalizer.transform(df)
    df = pd.DataFrame(df, columns = cs)

    df['Cases_per_mil'] = df_cases

    #Treinando
    lm = LinearRegression()
    lm.fit(df.iloc[2:, 2:-1], df.iloc[2:, 1])


def classify(dd, hb, pa, up):
    global df
    global lm

    df_test = normalizer.transform([[dd, hb, pa, up]])
    df_test = pd.DataFrame(df_test)
    
    predict = lm.predict(df_test)
    
    mudanca = 0
    menorDiferencaSegura = 9999
    menorDiferenca = 9999
    resulMaisProximo = 0
    
    for i in range(0, len(df.index)-1):
       
        dife = abs(df.iloc[i, 0] - predict[0])
        
        if df.iloc[i, -1] == 'Below' and dife < menorDiferencaSegura:
            menorDiferencaSegura = dife
            maiorSubDif = -1
            
            for ii in range(0, len(df.columns) - 3):
                subDif = abs(df.iloc[i, ii + 2] - df_test.iloc[0, ii])
                
                if subDif > maiorSubDif:
                    maiorSubDif = subDif
                    
                    if df.iloc[i, ii + 2] > df_test.iloc[0, ii]:
                        mudanca = (ii + 1)
                    else:
                        mudanca = -(ii + 1)
            
        if dife < menorDiferenca:
            menorDiferenca = dife
            resulMaisProximo = df.iloc[i, -1]
            
    return [resulMaisProximo, mudanca]

inialize()


data = {}

@app.route("/")
def index():
    return "<h1>EGG WAVE - FUNCIONANDO (Hackathon eddition v.5)</h1>"

@app.route("/sendData", methods=['POST'])
def sendData():
    info = request.data
    info = json.loads(info)
    ipv4 = request.remote_addr

    if not ipv4 in data:
        data[ipv4] = []

    data[ipv4].append(info)

    return "200"

@app.route("/getData", methods=['GET'])
def getData():
    ipv4 = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)   

    ret = {"ipv4": ipv4, "data": data[ipv4] if ipv4 in data else None}

    return json.dumps(ret)





@app.route("/submit", methods=['GET'])
@cross_origin()
def submit():
    density = request.form['density']
    icu = request.form['icu']
    elder = request.form['elder']
    population = request.form['population']

    return classify(density, icu, elder, population).to_json()
    
@app.route('/country/<name>', methods=['GET'])
@cross_origin()
def country(name):
    df = pd.read_csv('final.csv')
    df.set_index('Name', inplace=True)
    df.drop(df.columns[0], axis=1, inplace=True)
    return df.loc[name].to_json()







if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, threaded=True)