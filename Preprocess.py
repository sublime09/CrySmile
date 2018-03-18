import os
from pandas import DataFrame, read_pickle
from CSutils import emojiDict, ask

# Cols = ['id', 'screen_name', 'full_text']

def viewDataFrames():
	for emojiName in emojiDict:
		filename = 'data' + os.path.sep + emojiName + '.p'
		if os.path.isfile(filename):
			print("Reading", filename, "...")
			df = read_pickle(filename)
			print("#### The", emojiName, " Dataframe #####")
			print("\tshape=", df.shape, " size=", df.size)
			print("full_text Tweets:")
			for i in range(10):
				text = str(df['full_text'][i])
				print(text[:90])
			print()


def processDataFrames():
	for emojiName in emojiDict:
		filename = 'data' + os.path.sep + emojiName + '.p'
		if os.path.isfile(filename):
			print("Reading", filename, "...", end='')
			df = read_pickle(filename)
			print(emojiName, " is Dataframe:")
			print("columns:", df.columns)
			print("\tshape=", df.shape, " size=", df.size)
			print(df[0:10])


if __name__ == '__main__':
	viewDataFrames()