import re, os, codecs, pickle
import numpy
import pandas
import nltk
# from sklearn import feature_extraction
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
# import mpld3 # for visualization
from EmojiFrame import EmojiFrame, getAllEmojiFrames


def main():
	eFrame = getAllEmojiFrames()[0]
	print("EmojiFrame:", eFrame.emojiName)

	# dropping duplicate tweets (Retweets) removes half of tweets
	print("Before:", eFrame.frame.shape)
	eFrame.frame.drop_duplicates(subset='cleanTweet', inplace=True)
	print("After:", eFrame.frame.shape)

	# ids = eFrame.frame['tweetID'].values.tolist()
	# cleanTweets = eFrame.frame['cleanTweet'].values.tolist()
	# nltk.download('stopwords') # NEEDED ON FIRST RUN
	# nltk.download('punkt') # NEEDED ON FIRST RUN

	cleanTweets = eFrame.frame['cleanTweet']
	tokenCol = cleanTweets.apply(lambda row: tokenize(row))
	stemmedCol = tokenCol.apply(lambda row: stem(row))
	eFrame.frame['tokenTweet'] = tokenCol
	eFrame.frame['stemTweet'] = stemmedCol
	# print(eFrame)

	tokenVocab = set()
	stemmedVocab = set()
	for tokens in eFrame.frame['tokenTweet']:
		tokenVocab.update(tokens)
	for tokens in eFrame.frame['stemTweet']:
		stemmedVocab.update(tokens)

	vocab_frame = pandas.DataFrame({'words': tokenVocab}, index = stemmedVocab)
	print('There are', str(vocab_frame.shape[0]), 'items in vocab_frame')

	print("Token vocab:", len(tokenVocab))
	print("Stemmed vocab:", len(stemmedVocab))


	print("fitting...")
	#define vectorizer parameters
	cleanTweetsList = [str(x) for x in eFrame.frame['cleanTweet'].values.tolist()]
	for t in cleanTweetsList:
		a = str(t)



	# stopwords = nltk.corpus.stopwords.words('english') # same as option below
	opts = dict(max_df=0.6, max_features=200, use_idf=True)
	opts.update(dict(stop_words='english', ngram_range=(1,3)))
	opts['tokenizer'] = tokenize
	tfidf_vectorizer = TfidfVectorizer(**opts)
	tfidf_matrix = tfidf_vectorizer.fit_transform(cleanTweetsList)
	print("Done!")

	print("TFIDF matrix shape is", tfidf_matrix.shape)
	terms = tfidf_vectorizer.get_feature_names()
	print(terms)
	# dist = 1 - cosine_similarity(tfidf_matrix)



def tokenizeAndStem(text):
	return stem(tokenize(text))

def stem(tokens):
	stemmer = nltk.stem.snowball.SnowballStemmer("english")
	stems = [stemmer.stem(t) for t in tokens]
	return stems


def tokenize(text):
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
