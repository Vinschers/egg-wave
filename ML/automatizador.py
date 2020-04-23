import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report

df = None
x_train = None
x_test = None
y_train = None
y_test = None
predict = None

def acc():
	global predict
	global y_test

	cont = 0

	for i in range(len(predict)):
		p = predict[i]
		y = y_test.to_numpy()[i]
		if y == p:
			cont += 1
	return str(cont/len(predict) * 100) + "%"

def florestaAleatoria():
	global predict
	global x_train
	global y_train

	dtree = RandomForestClassifier(n_estimators = 200)
	dtree.fit(x_train, y_train)
	predict = dtree.predict(x_test)

	print("Floresta Aleatoria\t\t\t{}".format(acc()))



df = pd.read_csv(filepath_or_buffer=open('Teste0 - Dataset de Emocoes/emotions.csv', 'rb'))
x_train, x_test, y_train, y_test = train_test_split(df.drop('label',axis=1), df['label'], test_size=0.30)


#floresta aleatoria
florestaAleatoria()