import random
import pickle
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report

#tiposMl = ["ArvAle", "KNN", "SVM"]
tiposMl = ["ArvAle"]

df = None
x_train = None
x_test = None
y_train = None
y_test = None
predict = None
results = []

def acc():
	global predict
	global y_test

	cont = 0

	for i in range(len(predict)):
		p = predict[i]
		y = y_test.to_numpy()[i]
		if y == p:
			cont += 1
	return cont/len(predict) * 100

def florestaAleatoria():
	global predict
	global x_train
	global y_train
	global results

	dtree = RandomForestClassifier(n_estimators = 200)
	dtree.fit(x_train, y_train)
	results.append(dtree)

	predict = dtree.predict(x_test)
	arv_acc = acc()
	results.append(arv_acc)
	print("Floresta Aleatoria\t\t{}".format(arv_acc))

def knn():
	"""
	Colocar codigo
	"""
	return

def svm():
	"""
	Colocar codigo
	"""
	return	


#---Main---#
#Pegando o arquivo
print("-------------------------------------------")
print("Modo de leitura\n\r")
print("0 - buffer")
print("1 - csv")
print("-------------------------------------------")
modo = input()
path = input("PATH do arquivo: ")

if modo == "0":
	df = pd.read_csv(filepath_or_buffer=open(path, 'rb'))
elif modo == "1":
	df = pd.read_csv(path)

x_train, x_test, y_train, y_test = train_test_split(df.drop('label',axis=1), df['label'], test_size=0.30)

seed = str(random.randint(0, 1000000)) #codigo dos testes atuais

print("\n\r\n\r")
print("------------------------------------------")
print("Resultados\n\r")

#floresta aleatoria
florestaAleatoria()

#knn
knn()

#svm
svm()
print("------------------------------------------")

print("\n\r\n\r")
print("------------------------------------------")
print("Salvando dados\n\r")

res = input("Salvar relatorio?(s/n) ")
if res == "s":
	f = open("Relatorio" + seed + ".txt", "w")
	for i in range(0, len(tiposMl)):
		f.write(tiposMl[i] + ": " + str(results[1 + i * 2]))

	f.close()

res = input("Quais modelos deseja salvar?\n\r(indices separados por espacos): ").split()
if len(res) != 0:
	for modelo in res:
		i = int(modelo)
		pickle.dump(results[i * 2], open(tiposMl[i] + seed + '.sat', 'wb'))

print("------------------------------------------")