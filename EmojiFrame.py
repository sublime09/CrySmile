import re, os, pandas, pickle
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

def cleanTweet(tweet: str):
	urlPattern = '\\b(http|co/)\S*\\b'
	tweet = re.sub(urlPattern, '', tweet)
	retweetPattern = '\\bRT\\b'
	tweet = re.sub(retweetPattern, '', tweet)
	emojis = emojiDict.values()
	for emojiSymbol in emojis:
		replaceWith = emojiSymbol*3 
		pattern = emojiSymbol*2 + "+"
		tweet = re.sub(pattern, replaceWith, tweet)
	# maybe punct: # @ $ &
	punctPattern = '(\.|\,|\:|\;|\!)+'
	tweet = re.sub(punctPattern, '', tweet)
	extraSpacePattern = '\s\s+'
	tweet = re.sub(extraSpacePattern, ' ', tweet)
	tweet = tweet.strip()
	return tweet

if __name__ == '__main__':
	main()