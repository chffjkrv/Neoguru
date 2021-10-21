import json
import re
import nltk
from nltk.corpus import stopwords
from time import time
from sys import getsizeof
import os
import logging
import subprocess
import requests

from nltk.corpus.reader.framenet import FramenetCorpusReader

nada = input("Y tu que miras payaso? ")
nada = input("que coño quieres ")
nada = input("te lematizo o que ")
nada = input("que me ANSIo  ")
telematizo = input("que quieres que te lematize primero? ")
print('Voy \n')

logging.basicConfig(format="%(levelname)s - %(asctime)s: %(message)s", datefmt= '%H:%M:%S',filename='.\log\log.log', level=logging.DEBUG)
corpusTXT = open('.\corpus\corpusTXT.txt', 'w')
Prelematizado2FL = '.\Prelematizado\\'+telematizo+'_SW.txt'
Prelematizado = open(Prelematizado2FL, 'wb')
Lematizado2FL = '.\Lematizaciones\\'+telematizo+'Lematizado.txt'
Lematizado = open(Lematizado2FL, 'w')
Lematizado.close()
texto = ''
t_general = time()
t = time()

txt = open('.\Libros\\'+telematizo+'.txt', 'r').read()
txt = txt.lower()
txt = re.sub('[0-9]|[\(]|[\)]|[#]|[-]|[\[]|[\]]|[\']|[¿]|[?]|[¡]|[!]|[,]|[.]|[:]|[;]', ' ', txt)
corpusTXT.write(txt)

corpusTXT.close()
corpusTXT = open('.\corpus\corpusTXT.txt', 'r')
texto = corpusTXT.read()

SizeDataMb = getsizeof(texto)/1000000
logging.debug('[LEM]-->El texto tiene un tamanio en memoria de'+str(SizeDataMb)+' Mb')
logging.debug('[LEM]-->Normalizacion del texto terminada')
logging.debug('[LEM]-->Tiempo de normalizacion: {} mins'.format(round((time() - t) / 60, 2)))

print('Tokenizando frases... \n')
t = time()
frases = nltk.sent_tokenize(texto)
logging.debug('[LEM]-->Tokenizacion de frases completada') 
logging.debug('[LEM]-->Tiempo de Tokenizacion de frases: {} mins'.format(round((time() - t) / 60, 2)))

print('Tokenizando palabros... \n')
t = time()
palabras = [nltk.word_tokenize(sent) for sent in frases]
logging.debug('[LEM]-->Tokenizacion de palabras completada')
logging.debug('[LEM]-->Tiempo de Tokenizacion de palabras: {} mins'.format(round((time() - t) / 60, 2)))

print('withdrawing the palabras de parada (fuckoff maldita)... \n')
t = time()
for i in range(len(palabras)):
    palabras[i] = [w for w in palabras[i] if w not in stopwords.words('spanish')]
    Frase= ' '.join([str(item) for item in palabras[i]])
    Frase = bytearray(Frase.encode('utf-8'))
    Prelematizado.write(Frase)
    Frase = bytearray('\n'.encode('utf-8'))
    Prelematizado.write(Frase)

logging.debug('[LEM]-->Retiradas palabras de parada')
logging.debug('[LEM]-->Tiempo de Retiradas palabras de parada: {} mins \n'.format(round((time() - t) / 60, 2)))

Prelematizado.close()

logging.debug('[LEM]-->Tiempo de ejecución completa del lematizador: {} mins'.format(round((time() - t_general) / 60, 2)))
print('\n Mandando cosas para que te devuelvan cosas\n')
logging.debug('[LEM]--> Lanzamos la request')

files = {'file':open(Prelematizado2FL,'rb')}
params = {'outf':'tagged', 'format':'json'}
url = 'http://www.corpus.unam.mx/servicio-freeling/analyze.php'
r = requests.post(url, files=files, params=params)
logging.debug('[LEM]--> requests.post(url, files=files, params=params)')

obj = r.json()
jason=open('.\jasones\\'+telematizo+'Lematizado.json', 'w')
json.dump(obj, jason, indent=4)
jason.close()









#LEMATIZADOR :   http://www.corpus.unam.mx/servicio-freeling

#                subprocess.call('curl -F file=@'+Prelematizado2FL+' "http://www.corpus.unam.mx/servicio-freeling/analyze.php?outf=tagged&format=plain" -o ' + Lematizado2FL, shell = True)
