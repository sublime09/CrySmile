# use nltk to preprocess raw text and store processed text into a new csv file
# modify data preprocessing part and get rid of 000 amp 250????
# IMPORTANT: try another LDA visualization tool
# understand the meaning of relevance term 
# how to interpret LDA results???
# For the Future....



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
		sent = filter(None, re.split("[, \\n\.?]+", text))
		newsent = []
		for t in sent:
			newsent.append(t)
		stop_free = " ".join([i.lower() for i in newsent if i.lower() not in stop])
		punc_free = ''.join(ch for ch in stop_free if ch not in exclude)
		normalized = " ".join(lemma.lemmatize(word) for word in punc_free.split())			
		doc_completed.append(normalized)

doc_clean = [doc.split() for doc in doc_completed] 
# print(doc_clean)

# Creating the term dictionary of our courpus, where every unique term is assigned an index. 
dictionary = corpora.Dictionary(doc_clean)
dictionary.save('dictionary.dict')

# Converting list of documents (corpus) into Document Term Matrix using dictionary prepared above.
doc_term_matrix = [dictionary.doc2bow(doc) for doc in doc_clean]
corpora.MmCorpus.serialize('corpus.mm', doc_term_matrix)
print(doc_term_matrix)
# Creating the object for LDA model using gensim library
Lda = gensim.models.ldamodel.LdaModel

# Running and Trainign LDA model on the document term matrix.
ldamodel = Lda(doc_term_matrix, num_topics=5, id2word = dictionary, passes=150)
			
print(ldamodel.print_topics(num_topics=5, num_words=10))

for i in ldamodel.print_topics(): 
    for j in i: 
    	print(j)

ldamodel.save('topic.model')
