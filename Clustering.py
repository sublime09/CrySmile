import re, os, codecs, sys
import numpy
import pandas
import nltk
from nltk.tokenize import TweetTokenizer
# from sklearn import feature_extraction
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
# import mpld3 # for visualization
from EmojiFrame import EmojiFrame, getExistingEmojiFrames
from CSutils import millis, ask

def main():
	if ask("Try clustering of EmojiFrames?"):
		for ef in getExistingEmojiFrames():
			print("Now clustering the EmojiFrame:", ef.emojiName)
			cluster(ef)


def cluster(eFrame: EmojiFrame):
	# dropping duplicate tweets (Retweets) removes half of tweets
	eFrame.dropDuplicateTweets()
	# TODO: tweet tokenize; THEN drop punctuation

	# ids = eFrame.frame['tweetID'].values.tolist()
	# cleanTweets = eFrame.frame['cleanTweet'].values.tolist()
	# nltk.download('stopwords') # NEEDED ON FIRST RUN
	# nltk.download('punkt') # NEEDED ON FIRST RUN

	cleanTweets = eFrame.frame['cleanTweet']
	tokenCol = cleanTweets.apply(lambda row: basicTokenize(row))
	stemmedCol = tokenCol.apply(lambda row: stem(row))
	twTokenCol = cleanTweets.apply(lambda row: tweetTokenize(row))
	eFrame.frame['basicTokens'] = tokenCol
	eFrame.frame['setmmedTokens'] = stemmedCol
	eFrame.frame['tweetTokens'] = twTokenCol

	# tokenVocab = set()
	# stemmedVocab = set()
	# tweetVocab = set()
	# for tokens in eFrame.frame['basicTokens']:
	# 	tokenVocab.update(tokens)
	# for tokens in eFrame.frame['setmmedTokens']:
	# 	stemmedVocab.update(tokens)
	# for tokens in eFrame.frame['tweetTokens']:
	# 	tweetVocab.update(tokens)
	# #vocab_frame = pandas.DataFrame({'words': tokenVocab}, index = stemmedVocab)
	# print('There are', str(vocab_frame.shape[0]), 'items in vocab_frame')
	# print("Basic Token vocab:", len(tokenVocab))
	# print("Stemmed vocab:", len(stemmedVocab))
	# print("Tweet vocab:", len(tweetVocab))

	cleanTweetsList = [str(x) for x in eFrame.getCleanTweetsList()]

	start = millis()
	print("Fitting TFIDF takes... ", end='')
	sys.stdout.flush()
	#define vectorizer parameters
	opts = dict(max_features=200, use_idf=True)
	opts.update(dict(stop_words='english', ngram_range=(1,3)))
	opts['tokenizer'] = lambda x: tweetTokenize(x)
	tfidf_vectorizer = TfidfVectorizer(**opts)
	tfidf_matrix = tfidf_vectorizer.fit_transform(cleanTweetsList)
	print(millis() - start, "ms", sep='')

	print("TFIDF matrix shape is", tfidf_matrix.shape)
	terms = tfidf_vectorizer.get_feature_names()
	print(terms[:20])
	# dist = 1 - cosine_similarity(tfidf_matrix)


def tweetTokenize(text):
	text = str(text).lower()
	tknzr = TweetTokenizer(reduce_len=True)
	tokens = tknzr.tokenize(text)
	replacer = {"&":"and", '+':'plus', '@':'at', '/':'slash', '\\':'slash', '=':'equals'}
	tokens = [replacer[t] if t in replacer else t for t in tokens]
	# for badChar, goodChar in replacer.items():
	# 	tokens = [goodChar if t == badChar else t for t in tokens]
	badTokens = '\#$&\'()*-/1234567890\"[]\\<>?'
	tokens = [t for t in tokens if t not in badTokens]
	return tokens

def stem(tokens):
	stemmer = nltk.stem.snowball.SnowballStemmer("english")
	stems = [stemmer.stem(t) for t in tokens]
	return stems

def basicTokenize(text):
	# first tokenize by sentence, then by word to ensure that punctuation is caught as it's own token
	text = str(text).replace("\'", "")
	# TODO: add to preprocessing.  apostrophes are too much to handle
	tokens = [word.lower() for sent in nltk.sent_tokenize(text) for word in nltk.word_tokenize(sent)]

	filtered_tokens = []
	# filter out any tokens not containing letters (e.g., numeric tokens, raw punctuation)
	tokens = [t for t in tokens if re.search('[a-zA-Z]', t)]
	return tokens

if __name__ == '__main__':
	main()
