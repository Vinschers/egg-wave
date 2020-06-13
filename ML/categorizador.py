import random
import pickle
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.model_selection import GridSearchCV

nomesCategorizadores = ["./ML/676613ArvAle.sat"]

def categoriza(arq):
    predicts = -1 #onde sera guardado todos os resultados

    #Lendo
    df = pd.read_csv(arq)

    #Categotizando as emocoes (temporario) - Floresta Aleatoria
    with open(nomesCategorizadores[0], 'rb') as pickle_file:
        categorizador = pickle.load(pickle_file)
        predicts = categorizador.predict(df)

    #Gerando relatorio
    ret = {}
    for predict in predicts:
        for i in range(0, len(predict)):
            if predict[i] in ret:
                ret[predict[i]] += 1
            else:
                ret[predict[i]] = 1

    ret['Results'] = predicts

    return ret