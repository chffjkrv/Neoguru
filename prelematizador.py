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
corpus = [archivo for archivo in  os.listdir(os.getcwd()) if archivo[-3:] == 'txt']
corpusTXT = open('.\corpus\corpusTXT.txt', 'w')
BibliaCoranKitabi = open('.\BibliaCoranKitabi_SW.txt', 'w')
texto = ''
cont = 1
t_general = time()
t = time()
for archivo in corpus:

    txt = open(archivo, 'r').read()
#    txt = txt.lower()
#    txt = re.sub('[0-9]|[\(]|[\)]|[#]|[-]|[\[]|[\]]|[\']|[¿]|[?]|[¡]|[!]|[,]|[.]|[:]|[;]', ' ', txt)
    corpusTXT.write(txt)

    logging.debug('[LEM]-->van '+ str(cont) +' libros normalizados en memoria')
corpusTXT.close()

corpusTXT = open('.\corpus\corpusTXT.txt', 'r')

texto = corpusTXT.read()

SizeDataMb = getsizeof(texto)/1000000
logging.debug('[LEM]-->El texto tiene un tamanio en memoria de'+str(SizeDataMb)+' Mb')
logging.debug('[LEM]-->Normalizacion del texto terminada')
logging.debug('[LEM]-->Tiempo de normalizacion: {} mins'.format(round((time() - t) / 60, 2)))

t = time()
frases = nltk.sent_tokenize(texto)
logging.debug('[LEM]-->Tokenizacion de frases completada') 
logging.debug('[LEM]-->Tiempo de Tokenizacion de frases: {} mins'.format(round((time() - t) / 60, 2)))


t = time()
palabras = [nltk.word_tokenize(sent) for sent in frases]
logging.debug('[LEM]-->Tokenizacion de palabras completada')
logging.debug('[LEM]-->Tiempo de Tokenizacion de palabras: {} mins'.format(round((time() - t) / 60, 2)))

t = time()
for i in range(len(palabras)):
    palabras[i] = [w for w in palabras[i] if w not in stopwords.words('spanish')]
    BibliaCoranKitabi.write(' '.join([str(item) for item in palabras[i]]))
    BibliaCoranKitabi.write('\n')
    print(palabras[i])

logging.debug('[LEM]-->Retiradas palabras de parada')
logging.debug('[LEM]-->Tiempo de Retiradas palabras de parada: {} mins \n'.format(round((time() - t) / 60, 2)))

BibliaCoranKitabi.close()
logging.debug('[LEM]-->Tiempo de ejecución completa del lematizador: {} mins'.format(round((time() - t_general) / 60, 2)))








#LEMATIZADOR :   http://www.corpus.unam.mx/servicio-freeling
#                curl -F file=@BibliaCoranKitabi_SW.txt "http://www.corpus.unam.mx/servicio-freeling/analyze.php?outf=tagged&format=plain" -o BCK_Lematizado.txt