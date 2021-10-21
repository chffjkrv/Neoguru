import re
import nltk
import multiprocessing
from gensim.models import Word2Vec
from unicodedata import normalize
from nltk.corpus import stopwords
from time import time
from sys import getsizeof
import os
import logging
import sys
import codecs

logging.basicConfig(format="%(levelname)s - %(asctime)s: %(message)s", datefmt= '%H:%M:%S',filename='.\log\log.log', level=logging.DEBUG)
corpusdire = input("Que te modelo: ")
corpus = '.\Libros\\'+corpusdire+'.txt'
corpusTXT = open('.\corpus\corpusTXT.txt', 'w')
texto = ''
t = time()
txt = open(corpus, 'r').read()
txt = txt.lower()
txt = re.sub('[0-9]|[\(]|[\)]|[#]|[-]|[\[]|[\]]|[\']|[¿]|[?]|[¡]|[!]|[,]|[.]|[:]|[;]', ' ', txt)
corpusTXT.write(txt)
cont=+1
corpusTXT.close()

corpusTXT = open('.\corpus\corpusTXT.txt', 'r')

texto = corpusTXT.read()
print(texto)
SizeDataMb = getsizeof(texto)/1000000
logging.debug('[CreaModelos]--> El texto tiene un tamanio en memoria de'+str(SizeDataMb)+' Mb \n')
logging.debug('[CreaModelos]--> Normalizacion del texto terminada \n')
logging.debug('[CreaModelos]--> Tiempo de normalizacion: {} mins \n'.format(round((time() - t) / 60, 2)))

t = time()
frases = nltk.sent_tokenize(texto)
print(type(frases))
logging.debug('[CreaModelos]--> Tokenizacion de frases completada') 
logging.debug('[CreaModelos]--> Tiempo de Tokenizacion de frases: {} mins \n'.format(round((time() - t) / 60, 2)))

t = time()
palabras = [nltk.word_tokenize(sent) for sent in frases]
logging.debug('[CreaModelos]--> Tokenizacion de palabras completada \n')
logging.debug('[CreaModelos]--> Tiempo de Tokenizacion de palabras: {} mins \n'.format(round((time() - t) / 60, 2)))

t = time()

for i in range(len(palabras)):
    palabras[i] = [w for w in palabras[i] if w not in stopwords.words('spanish')]
logging.debug('[CreaModelos]--> Retiradas palabras de parada \n')
logging.debug('[CreaModelos]--> Tiempo de Retiradas palabras de parada: {} mins \n'.format(round((time() - t) / 60, 2)))
cores = multiprocessing.cpu_count()

t = time()
modeloW2V = Word2Vec(min_count=20,
                     window=2,
                     sample=6e-5, 
                     alpha=0.03, 
                     min_alpha=0.0007, 
                     negative=20,
                     workers=cores-1)

logging.debug('[CreaModelos]--> Creación del modelo \n')
logging.debug('[CreaModelos]--> Tiempo de creacion del modelo: {} mins \n'.format(round((time() - t) / 60, 2)))


t = time()
modeloW2V.build_vocab(palabras, progress_per=10000)
logging.debug('[CreaModelos]--> Generacion del vocabulario, completado. \n')
logging.debug('[CreaModelos]--> Tiempo de Generacion del vocabulario: {} mins \n'.format(round((time() - t) / 60, 2)))

t = time()
modeloW2V.train(palabras, total_examples=modeloW2V.corpus_count, epochs=30, report_delay=1)
logging.debug('[CreaModelos]--> Entrenamiento del modelo COMPLETADiSIMO \n')
logging.debug('[CreaModelos]--> Tiempo de entrenamiento: {} mins \n'.format(round((time() - t) / 60, 2)))

modeloW2V.save('.\Modelos\\'+corpusdire+'.model')





