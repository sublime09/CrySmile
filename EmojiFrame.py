import re, os, pandas, pickle
from pandas import DataFrame, read_pickle
from CSutils import emojiDict, ask, cleanTweet, millis

saveFolder = os.path.join('.', 'data', 'EmojiFrames')

def main():
	if ask("Make NEW EmojiFrames?"):
		for eFrame in getEmojiFramesFromRaw():
			print("NEW EmojiFrame:", eFrames.emojiName, end='')
			print(" shape is", eFrame.frame.shape)
			if ask("Print this EmojiFrame?"):
				print(eFrame)
				if ask("Save this EmojiFrame?"):
					eFrame.save()
	elif ask("See existing EmojiFrames?"):
		eFrames = getAllEmojiFrames()
		for ef in eFrames:
			print("EmojiFrame:", ef.emojiName, "shape is", ef.frame.shape)

def getEmojiFramesFromRaw():
	rawsFolder = os.path.join('.', 'data', 'RawTwitterDataframes')
	rawFilenames = os.listdir(path=rawsFolder)
	for fname in rawFilenames:
		emojiName = fname.split('.')[0]
		if emojiName in emojiDict:
			rawFrame = read_pickle(os.path.join(rawsFolder, fname))
			ef = EmojiFrame(emojiName, rawFrame)
			yield ef

def getAllEmojiFrames():
	start = millis()
	print("Loading EmojiFrames takes... ", end='')
	efFolder = os.path.join('.', 'data', 'EmojiFrames')
	efFiles = os.listdir(path=efFolder)
	efFiles = [os.path.join(efFolder, fname) for fname in efFiles]
	eFrames = list()
	for efFilename in efFiles:
		with open(efFilename, 'rb') as fileObj:
			eFrame = pickle.load(fileObj)	
			eFrames.append(eFrame)
	print(millis()-start, "ms", sep='')
	return eFrames

class EmojiFrame:
	def __init__(self, emojiName, rawDataFrame):
		self.emojiName = emojiName
		self.emojiSymbol = emojiDict[emojiName]
		goodData = self.getGoodData(rawDataFrame)
		self.frame = DataFrame(data=goodData)
		print("EmojiFrame created:", emojiName)

	def shape(self):
		return self.frame.shape

	def getCleanTweets(self):
		return self.frame['cleanTweet']

	def getCleanTweetsList(self):
		return self.getCleanTweets().values.tolist()

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
		# try:
		# 	goodData['rtID'] = rawFrame["retweeted_status"]["id"]
		# 	goodData['rtContext'] = rawFrame["retweeted_status"]["full_text"]
		# except:
		# 	pass
		goodData['cleanTweet'] = [cleanTweet(t) for t in rawTweets]
		goodData['isRetweet'] = ["RT " in t for t in rawTweets]
		return goodData

if __name__ == '__main__':
	main()