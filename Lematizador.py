import re
import nltk
from nltk.corpus import stopwords
from time import time
from sys import getsizeof
import os
import logging
import subprocess

from nltk.corpus.reader.framenet import FramenetCorpusReader

nada = input("Y tu que miras payaso? ")
nada = input("que coño quieres ")
nada = input("te lematizo o que ")
nada = input("que me ANSIo  ")
telematizo = input("que quieres que te lematize primero? ")
print('Voy \n')

logging.basicConfig(format="%(levelname)s - %(asctime)s: %(message)s", datefmt= '%H:%M:%S',filename='.\log\log.log', level=logging.DEBUG)
corpusTXT = open('.\corpus\corpusTXT.txt', 'w')
Prelematizado = open(telematizo+'_SW.txt', 'wb')
Lematizado = open(telematizo+'Lematizado.txt', 'w')
Lematizado.close()
Lematizado2FL = telematizo+'Lematizado.txt'
Prelematizado2FL = telematizo+'_SW.txt'
texto = ''
cont = 1
t_general = time()
t = time()

txt = open('.\Libros\\'+telematizo+'.txt', 'r').read()
txt = txt.lower()
txt = re.sub('[0-9]|[\(]|[\)]|[#]|[-]|[\[]|[\]]|[\']|[¿]|[?]|[¡]|[!]|[,]|[.]|[:]|[;]', ' ', txt)
corpusTXT.write(txt)
cont=+1
logging.debug('[LEM]-->van '+ str(cont) +' libros normalizados en memoria')

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
print('withdrawing the palabras de parada (fuckoff maldita)...\n')

Prelematizado.close()
logging.debug('[LEM]-->Tiempo de ejecución completa del lematizador: {} mins'.format(round((time() - t_general) / 60, 2)))
print('\n Mandando cosas para que te devuelvan cosas\n')
subprocess.call('curl -F file=@'+Prelematizado2FL+' "http://www.corpus.unam.mx/servicio-freeling/analyze.php?outf=tagged&format=plain" -o ' + Lematizado2FL, shell = True)







#LEMATIZADOR :   http://www.corpus.unam.mx/servicio-freeling

#                iconv -f ANSI_X3.110 -t UTF-8 -o BibliaCoranKitabi_SW.TXT
#                curl -F 'file=@BibliaCoranKitabi_SW.txt' "http://www.corpus.unam.mx/servicio-freeling/analyze.php?outf=tagged&format=plain" -o BCK_Lematizado.txtgit.txt

