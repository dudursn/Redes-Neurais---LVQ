import numpy as np
from random import random,choice
from math import sqrt
import dados

#Gera os valores de uma entrada(gera os pesos do vetor prototipo)
def vetor_aleatorio(dominio):
	valores = []
	numAtributos = len(dominio)
	minimo = dominio[0][0]
	maximo = dominio[0][1]
	for i in range(numAtributos):
		valor = minimo + ((maximo - minimo) * random())
		valores.append(valor)
	return valores

  
def imprimePrototipos(prototipos):
	for prototipo in prototipos:
		print(prototipo)
	

def dist_euclidiana(vetor1, vetor2):
	res = (np.subtract(vetor1, vetor2))**2
	soma = np.sum(res)
	return sqrt(soma)

#Cria os codebooks vectors ou protótipos
def inicializa_prototipos(classes, numPrototipos):
	dicionario = []
	#Os dados foram normalizados entre 0 e 1
	dominioDosAtributos = [[0,1] for x in range(4)]
	for i in range(numPrototipos):
		prototipo = {}
		classeSelecionada = choice(classes)
		prototipo['classe'] = classeSelecionada
		prototipo['vetor'] = vetor_aleatorio(dominioDosAtributos)
		dicionario.append(prototipo)
	return dicionario

#Faz o ranqueamento do melhor prototipo ou codebook
def pegar_unidade_de_melhor_correspondencia(dicionario, entrada):
	ranqueamento = []
	for prototipo in dicionario:
		distancia = dist_euclidiana(entrada['vetor'], prototipo['vetor'])
		ranqueamento.append((distancia, prototipo))
	melhorPrototipo = sorted(ranqueamento)[0][1]
	return melhorPrototipo

#Atualiza o melhor prototipo
def atualiza_prototipo(melhorPrototipo, entrada, novaTaxaDeApendizagem):
	numAtributos = len(melhorPrototipo['vetor'])
	for i in range(numAtributos):
		erro = entrada['vetor'][i] - melhorPrototipo['vetor'][i]
		if melhorPrototipo['classe'] == entrada['classe']:
			melhorPrototipo['vetor'][i] += novaTaxaDeApendizagem * erro
		else:
			melhorPrototipo['vetor'][i] -= novaTaxaDeApendizagem * erro

def treino(classes, baseTreino, numPrototipos, taxaDeAprendizagem):
	dicionario = inicializa_prototipos(classes, numPrototipos)
	novaTaxaDeApendizagem = taxaDeAprendizagem

	iteracoes = len(baseTreino)
	k = 0
	while(novaTaxaDeApendizagem>0.1):
		for i in range(iteracoes):
			entradaTreino = baseTreino[i]
			melhorPrototipo = pegar_unidade_de_melhor_correspondencia(dicionario, entradaTreino)
			novaTaxaDeApendizagem = taxaDeAprendizagem*(1.0 - (i/iteracoes))
			atualiza_prototipo(melhorPrototipo, entradaTreino, novaTaxaDeApendizagem)
			print("Iteracao", k,":",novaTaxaDeApendizagem)
			k+=1
		
		#print(" Classe do Melhor Prototipo:", melhorPrototipo['classe'], ", Classe da Entrada:",entradaTreino['classe'])
	return dicionario

def teste(prototipos, baseTeste):
	corretos = 0 
	numTestes = len(baseTeste)

	for i in range(numTestes):
		entradaTeste = baseTeste[i]
		melhorPrototipo = pegar_unidade_de_melhor_correspondencia(prototipos, entradaTeste)
		if melhorPrototipo['classe']== entradaTeste['classe']:
			corretos+=1
	print("Feito. Corretos:",corretos,"/",numTestes)
	acertos = (corretos/numTestes) * 100.0
	print("Acurácia: %.2f" % (acertos))

if __name__ == '__main__':
	# Dados
	baseTreino, baseTeste = dados.pegar_dados() 
	classes = ['setosa','versicolor','virginica']
	# Parametros do algoritmo
	taxaDeAprendizagem = 0.3
	numPrototipos = 10
	#Executar o algoritmo
	dicionario = treino(classes ,baseTreino, numPrototipos, taxaDeAprendizagem)
	teste(dicionario, baseTeste)
	imprimePrototipos(dicionario)
	