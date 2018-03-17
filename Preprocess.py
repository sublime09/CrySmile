import os
from pandas import DataFrame, read_pickle
from CSutils import emojiDict, ask

# Cols = ['id', 'screen_name', 'full_text']

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
