#import libraries like csv, numpy, etc
from sklearn.manifold import TSNE
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

# read the csv file and get the emotion_matrix(22886*6)
# ...
# ...

#Kmeans algorithm
kmeans = KMeans(n_clusters=4, random_state=0).fit(emotion_matrix)
print(kmeans.labels_)
print(kmeans.cluster_centers_)

#TSNE
X = TSNE(n_components=2).fit_transform(emotion_matrix)
print(X.shape)
plt.scatter(X[:,0], X[:,1], alpha=0.5)
plt.show()