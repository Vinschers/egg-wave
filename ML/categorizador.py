import random
import pickle
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.model_selection import GridSearchCV

colunasAPredizer = []
colunasADroppar = []

def categoriza(arq):
    #Lendo
    df = pd.read_csv(arq)

    return "Banana dancando"