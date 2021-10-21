
from gensim.test.utils import common_texts
from gensim.models import Word2Vec


model = Word2Vec.load("BibliaCoranKitabi.model")
sim_words = model.wv.most_similar('dios')


sims = model.wv.most_similar(positive=['king', 'woman'],negative=['man'])