import os
from twython import Twython
from pandas import DataFrame, read_pickle
from CSutils import emojiDict, getTwitter

# ''' ########### REMEMBER: #################'''
# '''MAX Number of Search Requests within 15-min window: 450'''
# '''We will get BLACKLISTED if we abuse the Twitter API'''
# ''' The secret file is NOT PUBLIC to avoid abuse of our Twitter access'''

class QueryTwitter:
	twitter = getTwitter()
	# default parameters for a query:
	qParams = dict(count='100', \
		lang='en', \
		result_type='recent', \
		tweet_mode='extended')
	# max count is 100!!!!

	def __init__(self, name, query):
		self.name = name
		self.query = query
		self.result = None


	def doQuery(self):
		# self.qParams['q'] = self.query
		jsonResult = self.twitter.search(q=self.query, **self.qParams)
		self.result = jsonResult


	def getJSONresult(self):
		if self.result == None:
			self.doQuery()
		return self.result


	def getDataFrame(self):
		tweetRows = self.getJSONresult()["statuses"]
		df = DataFrame.from_dict(tweetRows)

		screen_names = [r['screen_name'] for r in df['user']]
		goodCols = ['id', 'full_text']

		df = df[goodCols]
		df.insert(1, 'screen_name', screen_names, True)

		return df


	def saveDataFrame(self):
		df = self.getDataFrame()
		filepath = 'data'+os.path.sep+self.name+'.p'
		if os.path.isfile(filepath):
			print("Saving UPDATE", filepath, "...", end='')
			oldDF = read_pickle(filepath)
			df = df.append(oldDF)
		else:
			print("Saving NEW", filepath, "...", end='')

		df.drop_duplicates(subset='id', inplace=True)
		df.to_pickle(filepath)
		print("Done!")