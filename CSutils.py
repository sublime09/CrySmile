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

def ask(*question):
	print(*question)
	response = input("(yes/no) >>>")
	response = response.strip().lower()
	if response not in ['yes', 'no']:
		print("ASSUMING NO")
	return response == "yes"


def getTwitter():
	# reading the secrets....
	secretFilename = 'secret.txt'
	with open(secretFilename, 'r') as f:
		APP_KEY = f.readline().strip()
		APP_SECRET = f.readline().strip()
		ACCESS_TOKEN = f.readline().strip()
	twitter = Twython(APP_KEY, access_token=ACCESS_TOKEN)
	return twitter


def printDictLevels(d, base=''):
	for key in d:
		if type(d[key]) == type(dict()):
			printDictLevels(d[key], base+"["+key+"]")
		else:
			print(base, ":", d[key], sep='')
