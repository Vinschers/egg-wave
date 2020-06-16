import random
import pickle
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.model_selection import GridSearchCV 

import warnings
warnings.filterwarnings("ignore")

colunasADroppar = [-1]
colunaResultado = ''

tiposMl = ["ArvAle", "KNN", "SVM"] #Nomes dos modelos sendo usados ATUALMENTE -> nao colocar nomes alem dos que realmente sao chamados
configs = [200, 5] #Configuracoes padrao -> 0 - Numeros de arvores de decisao; 1 - 'k' do knn
                                         

df = None
x_train = None
x_test = None
y_train = None
y_test = None
predict = None
results = [] #Indices pares - modelos; indices impares - porcentagens de precisao

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
	global configs

	dtree = RandomForestClassifier(n_estimators = configs[0])
	dtree.fit(x_train, y_train)
	results.append(dtree)

	predict = dtree.predict(x_test)

	arv_acc = acc()
	results.append(arv_acc)
	print("Floresta Aleatoria\t\t{}".format(arv_acc))

def knn():
	global predict
	global x_train
	global y_train
	global results
	global configs

	scaler = StandardScaler()
	scaler.fit(df[[colunaResultado]])
	scaled_features = scaler.transform(df.drop('colunaResultado',axis=1))
	df.param = pd.DataFrame(scaled_features, columns=df.columns[:-1])

	knn = KNeighborsClassifier(n_neighbors=configs[1])
	knn.fit(x_train, y_train)
	results.append(knn)
	predict = knn.predict(x_test)

	knn_acc = acc()
	results.append(knn_acc)
	print("KNN\t\t\t\t{}".format(knn_acc))

def svm():
	global predict
	global x_train
	global y_train
	global results
	global configs

	param_grid = {'C': [0.1,1, 10, 100, 1000], 'gamma': [1,0.1,0.01,0.001,0.0001], 'kernel': ['rbf']}
	
	grid = GridSearchCV(SVC(),param_grid,refit=True,verbose=3)
	grid.fit(x_train,y_train)
	results.append(grid)
	predict = grid.predict(x_test)

	grid_acc = acc()
	results.append(grid_acc)
	print("SVM\t\t\t\t{}".format(grid_acc))


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

#Qual coluna usar
print("\n\r\n\r")
print("------------------------------------------")
print("Coluna a predizer\n\r")

colunaResultado = input("Nome da coluna a predizer: ")

print("------------------------------------------")

x_train, x_test, y_train, y_test = train_test_split(df.drop(df.columns[colunasADroppar],axis=1), df[colunaResultado], test_size=0.30)

seed = str(random.randint(0, 1000000)) #codigo dos testes atuais

#Configuracoes
print("\n\r\n\r")
print("------------------------------------------")
print("Configuracoes\n\r")

if input("Deseja alterar configuracoes avancadas?(s/n): ") == "s":
	res = input("Numero de arvores de decisao: ")
	if res != "":
		configs[0] = int(res)

	res = input("Valor de k(KNN): ")
	if res != "":
		configs[1] = int(res)
print("------------------------------------------")

#Resultados
print("\n\r\n\r")
print("------------------------------------------")
print("Resultados\n\r")

#floresta aleatoria
florestaAleatoria()

#knn
knn()

#svm
#svm()
print("------------------------------------------")


#Salvando
print("\n\r\n\r")
print("------------------------------------------")
print("Salvando dados\n\r")

res = input("Salvar relatorio?(s/n): ")
if res == "s":
	f = open(seed + colunaResultado + "Relatorio" + ".txt", "w")
	for i in range(0, len(tiposMl)):
		f.write(tiposMl[i] + ": " + str(results[1 + i * 2]))
		f.write('\n')

	f.close()

res = input("Quais modelos deseja salvar?\n\r(indices separados por espacos): ").split()
if len(res) != 0:
	for modelo in res:
		i = int(modelo)
		pickle.dump(results[i * 2], open(seed + tiposMl[i] + colunaResultado + '.sat', 'wb'))
print("------------------------------------------")