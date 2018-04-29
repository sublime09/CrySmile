import re, os, codecs, sys
import numpy as np
import pandas as pd
from timeit import timeit
from itertools import cycle

from nltk.tokenize import TweetTokenizer
from scipy import linalg
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.cluster import MeanShift, estimate_bandwidth
from sklearn.mixture import GaussianMixture, BayesianGaussianMixture
from sklearn.manifold import MDS
from sklearn.decomposition import PCA

import matplotlib.pyplot as plt
import matplotlib.cm as cm
from matplotlib.patches import Ellipse

from EmojiFrame import EmojiFrame, getExistingEmojiFrames
from CSutils import millis, ask, wrapper


def main():
	# if ask("Try clustering of EmojiFrames?"):
	for eFrame in getExistingEmojiFrames():
		eFrame = next(getExistingEmojiFrames())
		print("EmojiFrame: ", eFrame.emojiName, "shape=", eFrame.shape(), "Analysis:::")
		vecMatrix = getTFIDFmatrix(eFrame)
		print("MeanShift Clustering...")
		cluster(eFrame)
		return

def plot2DusingMDS(matrix, clusters):

	# this is for printing out to 2d matplotlib plots!
	precomputeDissimilarity = True
	df = None
	if precomputeDissimilarity:
		dist = 1 - cosine_similarity(tfidf_matrix)
		mds = MDS(n_components=2, dissimilarity="precomputed", random_state=1)
		pos = mds.fit_transform(dist)  # shape (n_components, n_samples)
		xs, ys = pos[:, 0], pos[:, 1]
		df = pd.DataFrame(dict(x=xs, y=ys, label=clusters, title=titles)) 
	else:
		mds = MDS(n_components=2, random_state=1)
		raise "Shape problem here?"
		pos = mds.fit_transform(matrix)  # shape (n_components, n_samples)
		xs, ys = pos[:, 0], pos[:, 1]
		df = pd.DataFrame(dict(x=xs, y=ys, label=clusters, title=titles)) 


def doMDSandPlot(title, simMatrix, clusterResults):
	n_samples = simMatrix.shape[0]
	print("Doing MDS with", n_samples, "samples")

	seed = np.random.RandomState(seed=1)
	opts = dict(n_components=2, max_iter=300, eps=1e-3, random_state=seed,
					   dissimilarity="precomputed", n_jobs=-2)
	mds = MDS(**opts)
	print("MDS Fitting in progress...", end='')
	pos = mds.fit(simMatrix).embedding_
	print("Done!")

	# Rotate the data
	clf = PCA(n_components=2)
	pos = clf.fit_transform(pos)

	xs, ys = pos[:, 0], pos[:, 1]
	labels = clusterResults.labels_
	uniques = np.unique(labels)
	
	colors = cm.rainbow(np.linspace(0, 1, len(uniques))) 

	fig = plt.figure(1)
	fig.suptitle(title, fontsize=20)
	plt.scatter(xs, ys, c=colors, s=15, lw=0, label='MDS')
	plt.show()


def clusterMeanShift(matrix):
	matrix = matrix.toarray() #must be dense array
	# The following bandwidth can be automatically detected using
	bandwidth = estimate_bandwidth(matrix, quantile=0.03, n_samples=1000)
	print("My bandwidth:", bandwidth)
	ms = MeanShift(bandwidth=bandwidth, bin_seeding=True, random_state=1)
	ms.fit(matrix)
	labels = ms.labels_
	cluster_centers = ms.cluster_centers_
	labels_unique = np.unique(labels)
	nClusters = len(labels_unique)
	print("Bandwidth= %d forms %s clusters" % (bandwidth, nClusters))

	""" Plot results of MeanShift
	plt.figure(1)
	plt.clf()
	colors = cycle('bgrcmykbgrcmykbgrcmykbgrcmyk')
	for k, col in zip(range(n_clusters_), colors):
	    my_members = labels == k
	    cluster_center = cluster_centers[k]
	    plt.plot(X[my_members, 0], X[my_members, 1], col + '.')
	    plt.plot(cluster_center[0], cluster_center[1], 'o', markerfacecolor=col,
	             markeredgecolor='k', markersize=14)
	plt.title('Estimated number of clusters: %d' % n_clusters_)
	plt.show()
	# """


def getTFIDFmatrix(eFrame: EmojiFrame):
	# import nltk
	# nltk.download('stopwords') # NEEDED ON FIRST RUN
	# nltk.download('punkt') # NEEDED ON FIRST RUN
	cleanTweetsList = [str(x) for x in eFrame.getCleanTweetsList()]
	cleanTweets = eFrame.frame['cleanTweet']
	twTokenCol = cleanTweets.apply(lambda row: tweetTokenize(row))
	eFrame.frame['tweetTokens'] = twTokenCol
	#define vectorizer parameters
	opts = dict(max_features=200, use_idf=True)
	opts.update(dict(stop_words='english', ngram_range=(1,2)))
	opts['tokenizer'] = lambda x: tweetTokenize(x)
	tfidf_vectorizer = TfidfVectorizer(**opts)
	tfidf_matrix = tfidf_vectorizer.fit_transform(cleanTweetsList)
	return tfidf_matrix

def tweetTokenize(text):
	text = str(text).lower()
	text = re.sub("'", "", text)
	tknzr = TweetTokenizer(reduce_len=True)
	tokens = tknzr.tokenize(text)
	replacer = {"&":"and", '+':'plus', '@':'at', '/':'slash', '\\':'slash', '=':'equals'}
	tokens = [replacer[t] if t in replacer else t for t in tokens]
	# for badChar, goodChar in replacer.items():
	# 	tokens = [goodChar if t == badChar else t for t in tokens]
	badTokens = '\#$&\'()*-/1234567890\"[]\\<>?'
	tokens = [t for t in tokens if len(t)>1 or t not in badTokens]
	return tokens

if __name__ == '__main__':
	main()
