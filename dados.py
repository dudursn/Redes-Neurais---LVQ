import numpy as np
from sklearn.model_selection import train_test_split

def normalizar_dados(data):
	for i in range(4):
		data[:,i] = (data[:,i] - min(data[:,i]))/(max(data[:,i]) - min(data[:,i]))
	return data

def pegar_dados():
	my_data = np.genfromtxt('iris.csv', delimiter=';')
	my_data = normalizar_dados(my_data)
	baseEntrada, baseSaida = my_data[:,:4], my_data[:,4]
	X, X_teste, Y, Y_teste = train_test_split(baseEntrada, baseSaida, test_size=0.3, random_state=0)

	baseTreino = []
	for i in range(len(Y)):
		instancia = {}
		instancia['classe'] = define_rotulo(int(Y[i]))
		instancia['vetor'] = X[i]
		baseTreino.append(instancia) 
	baseTeste = []
	for i in range(len(Y_teste)):
		instancia = {}
		instancia['classe'] = define_rotulo(int(Y_teste[i]))
		instancia['vetor'] = X_teste[i]
		baseTeste.append(instancia)

	return baseTreino, baseTeste

def define_rotulo(classe):
	if classe==1:
		return 'setosa'
	elif classe==2:
		return 'versicolor'
	else:
		return 'virginica'
