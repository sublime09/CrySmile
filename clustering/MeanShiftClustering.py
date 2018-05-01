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
		try:
			print("EmojiFrame: ", eFrame.emojiName, "shape=", eFrame.shape(), "Analysis:::")
			tfidf_matrix = getTFIDFmatrix(eFrame)
			simMatrix = 1 - cosine_similarity(tfidf_matrix)
			print("MeanShift Clustering...")
			clusterResults = clusterMeanShift(tfidf_matrix)
			# print("BayesianGaussianMixture with prior Dirichlet clustering...")
			# clusterVBGMM(tfidf_matrix)
			print("MDS example...")
			title = "EmojiFrame: "+eFrame.emojiName
			doMDSandPlot(title, simMatrix, clusterResults)
			print("Taking break...")
		except Exception as e:
			print("EmojiFrame", eFrame.emojiName, "FAILED and will skip:")
			print(e.message)


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
	samples = matrix.shape[0]

	# The following bandwidth can be automatically detected using
	opts = dict(quantile=0.023, n_samples=1000, random_state=1, n_jobs=-2)
	bandwidth = estimate_bandwidth(matrix, **opts)
	# print("My bandwidth:", bandwidth)
	ms = MeanShift(bandwidth=bandwidth, bin_seeding=True)
	print("MeanShift fitting in progress...", end='')
	ms.fit(matrix)
	print("Done!")
	labels = ms.labels_
	cluster_centers = ms.cluster_centers_
	labels_unique = np.unique(labels)
	nClusters = len(labels_unique)

	""" Plot results of MeanShift
	plt.figure(1)
	plt.clf()
	colors = cycle('bgrcmykbgrcmykbgrcmykbgrcmyk')
	for k, col in zip(range(nClusters), colors):
		my_members = labels == k
		cluster_center = cluster_centers[k]
		plt.plot(matrix[my_members, 0], matrix[my_members, 1], col + '.')
		plt.plot(cluster_center[0], cluster_center[1], 'o', markerfacecolor=col,
				 markeredgecolor='k', markersize=14)
	plt.title('Estimated number of clusters: %d' % nClusters)
	plt.show()
	# """
	
	outs = samples, bandwidth, nClusters
	print("Samples=%s Bandwidth=%s Clusters=%s" % outs)
	return ms


def clusterVBGMM(matrix):
	color_iter = cycle(['navy', 'c', 'cornflowerblue', 'gold','darkorange'])

	def plot_results(X, Y_, means, covariances, index, title):
		splot = plt.subplot(2, 1, 1 + index)
		for i, (mean, covar, color) in enumerate(zip(means, covariances, color_iter)):
			v, w = linalg.eigh(covar)
			v = 2. * np.sqrt(2.) * np.sqrt(v)
			u = w[0] / linalg.norm(w[0])
			# as the DP will not use every component it has access to
			# unless it needs it, we shouldn't plot the redundant components.
			if not np.any(Y_ == i):
				continue
			plt.scatter(X[Y_ == i, 0], X[Y_ == i, 1], .8, color=color)

			# Plot an ellipse to show the Gaussian component
			angle = np.arctan(u[1] / u[0])
			angle = 180. * angle / np.pi  # convert to degrees
			ell = Ellipse(mean, v[0], v[1], 180. + angle, color=color)
			ell.set_clip_box(splot.bbox)
			ell.set_alpha(0.5)
			splot.add_artist(ell)

		plt.xticks(())
		plt.yticks(())
		plt.title(title)

	# Number of samples per component
	n_samples = 500

	# Generate random sample, two components
	np.random.seed(0)
	C = np.array([[0., -0.1], [1.7, .4]])
	X = np.r_[np.dot(np.random.randn(n_samples, 2), C),
			  .7 * np.random.randn(n_samples, 2) + np.array([-6, 3])]

	# Fit a Gaussian mixture with EM using five components
	title = 'Gaussian Mixture'
	gmm = GaussianMixture(n_components=5, covariance_type='full').fit(X)
	plot_results(X, gmm.predict(X), gmm.means_, gmm.covariances_, 0,title)

	# Fit a Dirichlet process Gaussian mixture using five components
	title = 'Bayesian Gaussian Mixture with a Dirichlet process prior'
	dpgmm = BayesianGaussianMixture(n_components=5,covariance_type='full').fit(X)
	plot_results(X, dpgmm.predict(X), dpgmm.means_, dpgmm.covariances_, 1,title)
	plt.show()


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
