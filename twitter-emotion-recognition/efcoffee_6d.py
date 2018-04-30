import pickle
import nltk
# nltk.download()
from nltk.corpus import stopwords 
from nltk.stem.wordnet import WordNetLemmatizer
import string
import codecs
import gensim
from gensim import corpora

import csv
import re

from nltk import word_tokenize,sent_tokenize
from itertools import filterfalse
from collections import OrderedDict

import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)
from EmojiFrame import EmojiFrame

import pandas as pd
import numpy as np
from sklearn.manifold import TSNE
from sklearn.cluster import KMeans
from sklearn.cluster import MeanShift
from ggplot import *
import matplotlib.pyplot as plt

from emotion_predictor import EmotionPredictor
import tensorflow as tf
tf.python.control_flow_ops = tf


stop = set(stopwords.words('english'))
exclude = set(string.punctuation) 
lemma = WordNetLemmatizer()

doc_completed = []


emoji_pattern = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           "]+", flags=re.UNICODE)

with (open("../data/EmojiFrames/ef_Coffee.p", "rb")) as openfile:
	doc = pickle.load(openfile)
	doc.dropDuplicateTweets()
	tweets = doc.frame['cleanTweet'].values.tolist()
	for tweet in tweets:
		text = emoji_pattern.sub(r'', tweet)
		doc_completed.append(text)



# Predictor for Ekman's emotions in multiclass setting.
model = EmotionPredictor(classification='ekman', setting='mc')

probabilities = model.predict_probabilities(doc_completed)
# print(probabilities, '\n')
print(type(probabilities))
probabilities.to_csv('EmotionVectors/efcoffee_6d.csv')







###################################################
# emotion_vector = probabilities.iloc[:, 2:].values
# print(emotion_vector)

# https://pythonprogramming.net/hierarchical-clustering-mean-shift-machine-learning-tutorial/
# use other clustering techniques that can automatically find the number of clusters by themselves.

# kmeans = KMeans(n_clusters=4, random_state=0).fit(emotion_vector)
# print(kmeans.labels_)
# print(kmeans.cluster_centers_)

# X = TSNE(n_components=2).fit_transform(emotion_vector)
# print(X.shape)
# print(X)

# plt.scatter(X[:,0], X[:,1], alpha=0.5)
# plt.show()
# embeddings = model.embedd(tweets)
# print(embeddings, '\n')


