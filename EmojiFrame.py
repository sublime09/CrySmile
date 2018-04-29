import re, os, pandas, pickle
from pandas import DataFrame, read_pickle
from CSutils import emojiDict, ask, cleanTweet, millis
from QueryTwitter import getRawTwitterDataFrames

saveFolder = os.path.join('.', 'data', 'EmojiFrames')

def main():
	if ask("Make NEW EmojiFrames from raw DataFrames? (WARN: file collision causes overwrite)"):
		skip = ask("Skip all the prompts and just save automatically?")
		for eFrame in getEmojiFramesFromRawDFs():
			print("NEW EmojiFrame:", eFrame.emojiName, end='')
			print(" shape is", eFrame.frame.shape)
			if not skip and ask("Print this", eFrame.emojiName, "EmojiFrame?"):
				print(eFrame)
			if skip or ask("Save this", eFrame.emojiName, "EmojiFrame?"):
				eFrame.save()
	if ask("See existing EmojiFrames?"):
		start = millis()
		print("Loading EmojiFrames takes... ", end='')
		eFrames = list(getExistingEmojiFrames())
		print(millis()-start, "ms", sep='')
		for ef in eFrames:
			print("EmojiFrame:", ef.emojiName, "shape is", ef.frame.shape)

def getEmojiFramesFromRawDFs():
	for fname, df in getRawTwitterDataFrames():
		emojiName = fname.split('.')[0]
		if emojiName in emojiDict:
			ef = EmojiFrame(emojiName, df)
			yield ef
		else:
			print("Can't tell if emoji:", fname)

def getExistingEmojiFrames():
	efFiles = os.listdir(path=saveFolder)
	eFrames = list()
	for fname in efFiles:
		if re.match("ef_.*\\.p", fname):
			filepath = os.path.join(saveFolder, fname)
			with open(filepath, 'rb') as fileObj:
				try:
					eFrame = pickle.load(fileObj)
					if eFrame.emojiName in emojiDict:
						yield eFrame
					else:
						print("Can't tell if emoji:", eFrame.emojiName)
				except Exception as e:
					print("Error while loading EmojiFrame:", fname)
					print("Error:", e)
					print("Skipping".ljust(70, "."))

class EmojiFrame:
	def __init__(self, emojiName, rawDataFrame):
		self.emojiName = emojiName
		self.emojiSymbol = emojiDict[emojiName]
		goodData = self.getGoodData(rawDataFrame)
		self.frame = DataFrame(data=goodData)
		self.dropDuplicateTweets()
		print("EmojiFrame created:", emojiName, "with shape", self.frame.shape)

	def shape(self):
		return self.frame.shape

	def getCleanTweets(self):
		return self.frame['cleanTweet']

	def getCleanTweetsList(self):
		return self.getCleanTweets().values.tolist()

	def dropDuplicateTweets(self):
		original = self.frame.shape[0]
		self.frame.drop_duplicates(subset='cleanTweet', inplace=True)
		now = self.frame.shape[0]
		print("Dropping duplicates: %s -> %s tweets" % (original, now))

	def save(self, filepath=None):
		if filepath == None:
			filepath = os.path.join(saveFolder, 'ef_'+self.emojiName+'.p')
		with open(filepath, "wb") as fileObject:
			pickle.dump(self, fileObject)
		print("Saved:", filepath)

	def __repr__(self):
		width = 120
		title = ("EmojiFrame: "+self.emojiName).center(width//4)
		output = [title.center(width, '#')]
		with pandas.option_context('display.max_rows', 10, 'display.width', width):
			output.append(repr(self.frame))
		return '\n'.join(output)

	def getGoodData(self, rawFrame: DataFrame):
		goodData = dict()
		goodData['tweetID'] = rawFrame['id']
		goodData['dateCreated'] = rawFrame['created_at']
		rawTweets = rawFrame['full_text']
		goodData['rawTweet'] = rawTweets
		goodData['userName'] = [d['screen_name'] for d in rawFrame['user']]
		goodData['cleanTweet'] = [cleanTweet(t) for t in rawTweets]
		goodData['isRetweet'] = ["RT " in t for t in rawTweets]
		return goodData

if __name__ == '__main__':
	main()