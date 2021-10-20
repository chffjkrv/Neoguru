
from gensim.test.utils import common_texts
from gensim.models import Word2Vec


model = Word2Vec.load("ModeloBiblico2.model")
sim_words = model.wv.most_similar('dios')