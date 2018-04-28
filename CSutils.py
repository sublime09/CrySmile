import re
from time import time
from twython import Twython

# This is the name of an emoji followed its symbol
emojiDict = dict()
emojiDict['CrySmile']   = '😂'
emojiDict['LoudCry']    = '😭'
emojiDict['Cry']        = '😢'
emojiDict['SmileSmile'] = '😊'
emojiDict['Fire']       = '🔥'
emojiDict['ThumbsUp']   = '👍'
emojiDict['Heart']      = '❤'
emojiDict['Coffee']     = '☕'

twitter = None

def ask(*question):
	print(*question, end='?\n')
	response = input("(yes/no) >>> ")
	response = response.strip().lower()
	if response not in ['yes', 'no']:
		print("ASSUMING NO")
	return response == "yes"

def millis():
	return round(time() * 1000)

def getTwitter(twitter=twitter):
	if twitter == None:
		# reading the secrets....
		secretFilename = 'secret.txt'
		try:
			with open(secretFilename, 'r') as f:
				APP_KEY = f.readline().strip()
				APP_SECRET = f.readline().strip()
				ACCESS_TOKEN = f.readline().strip()
			twitter = Twython(APP_KEY, access_token=ACCESS_TOKEN)
		except Exception as e:
			print("Missing or invalid", secretFilename, "... exiting...")
			exit()
	return twitter

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
	return str(tweet)

def printDictLevels(d, base=''):
	for key in d:
		if type(d[key]) == type(dict()):
			printDictLevels(d[key], base+"["+key+"]")
		else:
			print(base, ":", d[key], sep='')

def wrapper(func, *args, **kwargs):
	def wrapped():
		return func(*args, **kwargs)
	return wrapped

	