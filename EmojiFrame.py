import os, pandas, pickle
from pandas import DataFrame, read_pickle
from CSutils import emojiDict, ask

def main():
	if ask("Make EmojiFrames?"):
		for emojiName in emojiDict:
			filepath = 'data'+os.path.sep+emojiName+'.p'
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
			filepath = 'data'+os.path.sep+"ef_"+self.emojiName+'.p'
		fileObject = open(filepath, "wb")
		pickle.dump(self, fileObject)
		fileObject.close()
		print("Saved:", filepath)


	def __repr__(self):
		output = list()
		output.append("%"*60+"The "+self.emojiName+" EmojiFrame:")
		# output.append("Shape:"+str(self.frame.shape))
		with pandas.option_context('display.max_rows', 10, 'display.width', 160):
			output.append(repr(self.frame))
		return '\n'.join(output)


	def getGoodData(self, rawFrame: DataFrame):
		goodData = dict()
		goodData['tweetID'] = rawFrame['id']
		goodData['dateCreated'] = rawFrame['created_at']
		rawTweets = rawFrame['full_text']
		# goodData['rawTweet'] = rawTweets
		goodData['userName'] = [d['screen_name'] for d in rawFrame['user']]
		try:
			goodData['rtID'] = rawFrame["retweeted_status"]["id"]
			goodData['rtContext'] = rawFrame["retweeted_status"]["full_text"]
		except:
			pass
		goodData['cleanTweet'] = [cleanTweet(t) for t in rawTweets]
		goodData['isRetweet'] = [t.startswith("RT ") for t in rawTweets]
		return goodData


def cleanTweet(rawTweet: str):
	rawTweet = rawTweet.lstrip("RT ")
	rawTweet = rawTweet.strip()
	for emojiSymbol in emojiDict.values():
		if emojiSymbol not in rawTweet:
			continue
		while emojiSymbol*10 in rawTweet:
			rawTweet = rawTweet.replace(emojiSymbol*10, emojiSymbol*5)
		while emojiSymbol*5 in rawTweet:
			rawTweet = rawTweet.replace(emojiSymbol*5, emojiSymbol*4)
	# todo: remove punctuation
	return rawTweet


if __name__ == '__main__':
	main()