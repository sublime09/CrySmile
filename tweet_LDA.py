# use nltk to preprocess raw text and store processed text into a new csv file
# modify data preprocessing part and get rid of 000 amp 250????
# IMPORTANT: try another LDA visualization tool
# understand the meaning of relevance term 
# how to interpret LDA results???
# For the Future....





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


stop = set(stopwords.words('english'))
exclude = set(string.punctuation) 
lemma = WordNetLemmatizer()

doc_completed = []


# Tweet preprocessing--- one tweet for each iteration and store all the preprocessed tweets in doc_completed.
# As long as all the collected tweets can be read and processed using the for loop below, you don't need to worry about the LDA part, 
# which starts with the list containing all processed tweets ----- doc_completed
with codecs.open('tweets.emojis-EN-#metoo_2017-1016_n28629.csv', "r",encoding='utf-8', errors='ignore') as fdata:
	reader = csv.DictReader(fdata)
	for row in reader:
		print(row['tweetid'])
		sent = filter(None, re.split("[, \\n\.?]+", row['text']))
		# print(re.findall(r"[\w']+", sent))
		# nltk.word_tokenize(sent)
		porter = nltk.PorterStemmer()
		newsent = []
		for t in sent:
			if t.startswith('co/'):
				pass
			elif len(t)>3 and t[3] == '>':
				pass
			elif t == 'u':
				pass
			elif t.startswith('https'):
				pass
			elif t.startswith('#') or t.startswith('@') or t.startswith('$') or t.startswith('&') or t[0].isdigit():
				pass
			elif re.search('<', t):
				pass
			# elif t.endswith('.'):
			# 	newsent.append(t[:-2])
			else:
				newsent.append(t)
		print(newsent);
			# count += 1
			# domain = OrderedDict([('tweetid', row['tweetid']),
	  #                 ('text', newsent),
	  #                 ('num.emojis', row['num.emojis']),
	  #                 ('emoji_names', row['emoji_names'])])
			# print(domain
		stop_free = " ".join([i.lower() for i in newsent if i.lower() not in stop])
		punc_free = ''.join(ch for ch in stop_free if ch not in exclude)
		normalized = " ".join(lemma.lemmatize(word) for word in punc_free.split())	
		print(normalized)			
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
ldamodel = Lda(doc_term_matrix, num_topics=3, id2word = dictionary, passes=100)
			
print(ldamodel.print_topics(num_topics=3, num_words=10))

for i in ldamodel.print_topics(): 
    for j in i: 
    	print(j)

ldamodel.save('topic.model')
