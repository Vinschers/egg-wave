from flask import Flask, jsonify, request, render_template, Response, send_file, stream_with_context, make_response
import pandas as pd
from sklearn import preprocessing
from sklearn.linear_model import LinearRegression
from flask_cors import CORS, cross_origin

#Control variables
path = './Hackathon/final.csv'
#drop = [0, 1, 5, 6, 7, 8, 9, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 22, 23, 24, 25, 26, 27, 28, 30, 31]
drop = [0, 3, 4, 5, 6, 7]
prever = [0, 1, -1] #Indexes of the new dfs

#Global variables
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

    #Reading
    df = pd.read_csv(path)
    
    #Rearranging columns
    df.drop(df.columns[drop], axis=1, inplace=True)

    df_cases = df.iloc[:, 6]
    df.drop('Deaths_per_mil', axis=1, inplace=True)

    cs = df.columns

    #Normalization
    normalizer = preprocessing.Normalizer().fit(df)
    df = normalizer.transform(df)
    df = pd.DataFrame(df, columns = cs)

    df['Deaths_per_mil'] = df_cases

    #Training
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

def routes(app):
    cors = CORS(app, resources={r"/api/*": {"origins": "*"}}, support_credentials=True)
    app.config['CORS_HEADERS'] = 'Content-Type'
    @app.route("/submit", methods=['GET'])
    @cross_origin()
    def submit():
        density = request.args.get('density')
        icu = request.args.get('icu')
        elder = request.args.get('elder')
        population = request.args.get('population')

        return jsonify(classify(density, icu, elder, population))
        
    @app.route('/country/<name>', methods=['GET'])
    @cross_origin()
    def country(name):
        df = pd.read_csv(path)
        df.set_index('Name', inplace=True)
        return df.loc[name].to_json()