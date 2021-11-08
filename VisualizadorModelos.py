import matplotlib.pyplot as plt
from sklearn.decomposition import IncrementalPCA    # inital reduction
from sklearn.manifold import TSNE                   # final reduction
import numpy as np                                  # array handling
from gensim.models import Word2Vec
import pandas as pd

model = Word2Vec.load(".\Modelos\BibliaCoranKitabi.model")
vocab = list(model.wv.key_to_index)
X = model.wv[vocab]
tsne = TSNE(n_components=2)
X_tsne = tsne.fit_transform(X)
df = pd.DataFrame(X_tsne, index=vocab, columns=['x', 'y'])
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)

ax.scatter(df['x'], df['y'])

for word, pos in df.iterrows():
    ax.annotate(word, pos)

fig.savefig('representacion2d.jpeg', fomrat='jpeg', quality = 95)
plt.show()
