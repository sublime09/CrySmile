import os, time
from twython import Twython
from pandas import DataFrame, read_pickle
from CSutils import emojiDict, getTwitter, ask

# ''' ########### REMEMBER: #################'''
# '''MAX Number of Search Requests within 15-min window: 450'''
# '''We will get BLACKLISTED if we abuse the Twitter API'''
# ''' The secret file is NOT PUBLIC to avoid abuse of our Twitter access by attackers'''

def main():
	if ask("Do Full Query Process?"):
		queryTime = int(input("Enter seconds of query process:"))
		doQueryProcess(queryTime)
	elif ask("Do Small QueryTwitter Test?"):
		smallTest()


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
		return df


	def saveDataFrame(self, filepath=None):
		df = self.getDataFrame()
		if filepath == None:
			filepath = os.path.sep.join(['data', 'RawTwitterDataframes', self.name+'.p'])
		if os.path.isfile(filepath):
			print("Saving UPDATE", filepath, "...", end='')
			oldDF = read_pickle(filepath)
			df = df.append(oldDF)
		else:
			print("Saving NEW", filepath, "...", end='')

		df.drop_duplicates(subset='id', inplace=True)
		df.to_pickle(filepath)
		print("Done!")



def doQueryProcess(processTime=3600):
	maxQsecRate = (400 / 15.0) / 60.0
	totalQueries = int(maxQsecRate * processTime)
	sleepSeconds = processTime / float(totalQueries)
	emojiNames = list(emojiDict.keys())

	if ask("Do", totalQueries, "queries over", processTime, "seconds?"):
		for qNum in range(totalQueries):
			emojiNum = qNum % len(emojiNames)
			emojiName = emojiNames[emojiNum]
			emojiSearchTerm = emojiDict[emojiName]
			query = QueryTwitter(emojiName, emojiSearchTerm)
			query.doQuery()
			query.saveDataFrame()
			time.sleep(sleepSeconds)
		print("finished!!!!!")
	else:
		print("Cancelled")


def smallTest():
	print("Testing small query of CrySmile...")
	emojiName = "CrySmile"
	emojiSymbol = emojiDict[emojiName]
	qt = QueryTwitter(emojiName, emojiSymbol)
	qt.qParams["count"] = 5
	qt.doQuery()
	df = qt.getDataFrame()
	print("Raw TESTCrySmile DataFrame:")
	print("#### The", emojiName, " Dataframe #####")
	print("\tshape=", df.shape, " size=", df.size)
	for col in df.columns:
		printDictLevels(df[col])
	# print("full_text Tweets:")
	# for i in range(8):
	# 	text = str(df['full_text'][i])
	# 	print(text[:90], "......")
	print()


if __name__ == '__main__':
	main()
