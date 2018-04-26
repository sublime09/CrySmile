import re, os, pandas, pickle
from pandas import DataFrame, read_pickle
from CSutils import emojiDict, ask, cleanTweet, millis

def main():
	if ask("Make EmojiFrames?"):
		for emojiName in emojiDict:
			filepath = os.path.join('data', 'RawTwitterDataframes', emojiName+'.p')
			if os.path.isfile(filepath):
				rawFrame = read_pickle(filepath)
				ef = EmojiFrame(emojiName, rawFrame)
				ef.save()
				print(ef)


class EmojiFrame:
	def __init__(self, emojiName, rawDataFrame):
		self.emojiName = emojiName
		self.emojiSymbol = emojiDict[emojiName]
		goodData = self.getGoodData(rawDataFrame)
		self.frame = DataFrame(data=goodData)
		print("EmojiFrame created:", emojiName)

	def save(self, filepath=None):
		if filepath == None:
			filepath = os.path.join('data', 'EmojiFrames', 'ef_'+self.emojiName+'.p')
		with open(filepath, "wb") as fileObject:
			pickle.dump(self, fileObject)
		print("Saved:", filepath)

	def __repr__(self):
		output = list()
		width = 120
		title = ' ' + self.emojiName+" EmojiFrame" + ' '
		filler = '@'* int((width - len(title)) / 2)
		output.append(filler + title + filler)
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
		try:
			goodData['rtID'] = rawFrame["retweeted_status"]["id"]
			goodData['rtContext'] = rawFrame["retweeted_status"]["full_text"]
		except:
			pass
		goodData['cleanTweet'] = [cleanTweet(t) for t in rawTweets]
		goodData['isRetweet'] = ["RT " in t for t in rawTweets]
		return goodData

def getAllEmojiFrames():
	efFolder = os.path.join('.', 'data', 'EmojiFrames')
	efFiles = os.listdir(path=efFolder)
	efFiles = [os.path.join(efFolder, fname) for fname in efFiles]
	eFrames = list()
	for efFilename in efFiles:
		with open(efFilename, 'rb') as fileObj:
			eFrame = pickle.load(fileObj)	
			eFrames.append(eFrame)
	return eFrames


if __name__ == '__main__':
	main()