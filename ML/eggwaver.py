#Imports
import pandas as pd
import numpy as np

from sklearn.ensemble import RandomForestClassifier

from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split
import pickle

class EggWaver:
    def __init__(self):
        self.modelo = None

    def treina_modelo(self, data_x, data_y, ml_type, test_size = 0.2, random_state = None, verbose = 2, n = 50):
        #Dividindo os dados
        train_x, test_x, train_y, test_y = train_test_split(data_x, data_y, test_size = test_size, random_state = random_state)

        #Treinando o modelo
        if ml_type == "RandomForestClassifier":
            self.modelo = RandomForestClassifier(n_estimators = n, verbose = verbose, n_jobs = -1, random_state = random_state)

        self.modelo.fit(train_x, train_y)

        #Retornando precisao de teste
        predict = modelo.predict(test_x)

        return classification_report(test_y, predict)

    def predict_bloco(self, data_x, freq = 1):
        #Existe um modelo para fazer a predicao?
        if self.modelo is None:
            raise Exception("Modelo nao existe")

        #Fazendo a predicao
        predict = self.modelo.predict_proba(data_x)

        #Calculando a resposta para cada trecho conforme a confianca do modelo
        ret = []
    
        for ini in range(0, len(data_x.index), freq):
            confiancaPorTrecho = predict[ini : min(ini + freq, len(data_x.index)), ].mean(axis=0) #Fazendo a media dos
                                                                                                  #freq dados seguidos

            ret.append(confiancaPorTrecho)
        
        return ret

    def salvar_modelo(self, arq):
        #Existe um modelo para salvar?
        if self.modelo is None:
            raise Exception("Modelo nao existe")

        #Salvando o modelo
        pickle.dump(self.modelo, open(arq + '.sat', 'wb'))

    def retomar_modelo(self, arq):
        #Lendo o modelo
        self.modelo = pickle.load(open(arq + '.sat', 'rb'))