import bs4 as bs
import urllib.request
import re
import nltk
import multiprocessing
from gensim.models import Word2Vec
from unicodedata import normalize
from nltk.corpus import stopwords
from time import time
from collections import defaultdict  # For word frequency
import spacy 

import logging  

logging.basicConfig(format="%(levelname)s - %(asctime)s: %(message)s", datefmt= '%H:%M:%S', level=logging.INFO)

t = time()

scrapped_data1 = urllib.request.urlopen('https://es.wikipedia.org/wiki/AZCA')
scrapped_data2 = urllib.request.urlopen('http://www.secretosdemadrid.es/por-que-azca-se-llama-asi/')

articulo1 = scrapped_data1.read()
articulo2 = scrapped_data2.read()

articulo_parseado1 = bs.BeautifulSoup(articulo1, 'lxml')
articulo_parseado2 = bs.BeautifulSoup(articulo2, 'lxml')

parrafos = articulo_parseado1.find_all('p') + articulo_parseado2.find_all('p')

txt_articulo= ""

for p in parrafos:
    txt_articulo += p.text

txt_procesado = txt_articulo.lower()
txt_procesado = re.sub(
        r"([^n\u0300-\u036f]|n(?!\u0303(?![\u0300-\u036f])))[\u0300-\u036f]+", r"\1", 
        normalize( "NFD", txt_procesado), 0, re.I
    )
txt_procesado =normalize( 'NFC', txt_procesado)


txt_procesado = re.sub(r'\[(\d+)\]', '', txt_procesado)

frases = nltk.sent_tokenize(txt_procesado)
palabras = [nltk.word_tokenize(sent) for sent in frases]

for i in range(len(palabras)):
    palabras[i] = [w for w in palabras[i] if w not in stopwords.words('spanish')]

cores = multiprocessing.cpu_count()

modeloW2V = Word2Vec(min_count=20,
                     window=2,
                     sample=6e-5, 
                     alpha=0.03, 
                     min_alpha=0.0007, 
                     negative=20,
                     workers=cores-1)

modeloW2V.build_vocab(palabras, progress_per=10000)

modeloW2V.train(palabras, total_examples=modeloW2V.corpus_count, epochs=30, report_delay=1)

modeloW2V.wv.most_similar(positive=["zona"])


print('Time to train the model: {} mins'.format(round((time() - t) / 60, 2)))

