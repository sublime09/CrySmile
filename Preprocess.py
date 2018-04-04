import os
from pandas import DataFrame, read_pickle
from CSutils import emojiDict, ask
from EmojiFrame import EmojiFrame

# Cols = ['id', 'screen_name', 'full_text', 'is_retweet']


def getDataFrames():
	for emojiName in emojiDict:
		filename = 'data' + os.path.sep + emojiName + '.p'
		if os.path.isfile(filename):
			df = read_pickle(filename)
			df.emojiName = emojiName
			df.emojiSymbol = emojiDict[emojiName]
			yield df
	

def viewDataFrames():
	for df in getDataFrames():
		print("#### The", df.emojiName, " Dataframe #####")
		print("\tshape=", df.shape, " size=", df.size)
		print("Columns:", df.columns)
		print(df[:3])
		print("full_text Tweets:")
		for i in range(3):
			text = str(df['full_text'][i])
			print(text[:90], "......")
		print()


def processDataFrames():
	for df in getDataFrames():
		print("Processing Dataframe:", df.emojiName)
		fixRT(df)
		removePunct(df)
		sepTerms(df)


def fixRT(df):
	# Cols = ['id', 'screen_name', 'full_text', 'is_retweet']
	numRows, numCols = df.shape
	for i in range(numRows):
		rawText = str(df['full_text'][i])
		if rawText.startswith("RT @"):
			print("Before:", df["full_text"][i])
			df["realText"][i] = rawText.lstrip(": ")
			print("After:", df["full_text"][i])


def removePunct(df):
	pass


def sepTerms(df):
	pass


if __name__ == '__main__':
	viewDataFrames()
	if ask("Process Data Frames?"):
		name = "CrySmile"
		ef = EmojiFrame(name)
		print(ef.frame[:3])
		# processDataFrames()

