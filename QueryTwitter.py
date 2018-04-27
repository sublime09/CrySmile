import os, time
from itertools import cycle
from twython import Twython
from pandas import DataFrame, read_pickle
from CSutils import emojiDict, getTwitter, ask, millis

# ''' ########### REMEMBER: #################'''
# '''MAX Number of Search Requests within 15-min window: 450'''
# '''We will get BLACKLISTED if we abuse the Twitter API'''
# ''' The secret file is NOT PUBLIC to avoid abuse of our Twitter access by attackers'''

saveFolder = os.path.join('.', 'data', 'RawTwitterDataframes')

def main():
	if ask("Query Twitter for Emojis?"):
		print("EmojiDict=", emojiDict)
		queryTime = int(input("Enter seconds of duration (zero is forever):"))
		doQueryProcess(queryTime)
	elif ask("View available raw Twitter Dataframes?"):
		print("Raw Twitter DataFrames:")
		for fname, rawFrame in getRawTwitterDataFrames():
			print(fname, "shape is", rawFrame.shape)
		print("Done!")
	# elif ask("Do Small QueryTwitter Test?"):
	# 	smallTest()


def getRawTwitterDataFrames():
	rawDFFilenames = os.listdir(path=saveFolder)
	for fname in rawDFFilenames:
		if fname.split('.')[0] in emojiDict:
			filepath = os.path.join(saveFolder, fname)
			rawFrame = read_pickle(filepath)
			yield (fname, rawFrame)
		else:
			print("Can't tell if emoji:", fname)


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
		self.result = 111
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

	def saveDataFrame(self, folder=saveFolder):
		filename = self.name + ".p"
		filepath = os.path.join(folder, filename)
		df = self.getDataFrame()
		if os.path.isfile(filepath):
			print("Saving UPDATE", filename.ljust(20), "..." , end='')
			oldDF = read_pickle(filepath)
			df = df.append(oldDF)
		else:
			print("Saving NEW", filepath, "...", end='')
		df.drop_duplicates(subset='id', inplace=True)
		df.to_pickle(filepath)
		print("Done! shape is", df.shape)


def doQueryProcess(duration=0):
	# MAX ALLOWED: 400 queries within 15 minutes
	sleepPerQuery = (15.0 / 400) * 60 
	emojiDictCycler = cycle(emojiDict.items())
	firstEmojiName = list(emojiDict.keys())[0]

	dStr = "forever" if duration == 0 else str(duration) + " seconds"
	if ask("Query Twitter every", sleepPerQuery, "seconds for", dStr):
		end = millis() + 1000 * duration
		errorsInRow = 0
		while duration == 0 or millis() < end:
			emojiName, emojiSymbol = next(emojiDictCycler)
			qt = QueryTwitter(emojiName, emojiSymbol)
			try:
				qt.doQuery()
				qt.saveDataFrame()
				errorsInRow = 0
			except Exception as e:
				print("ERROR:", e)
				errorsInRow += 1
			if emojiName == firstEmojiName:
				print("Press Ctrl+c to exit at any time")
			if errorsInRow == 10:
				print("Too many errors in a row!!!  We should exit...")
				exit(1)
			time.sleep(sleepPerQuery)
		print("Finished!!!!!")
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
