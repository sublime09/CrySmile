from twython import Twython

# This is the name of an emoji followed by all of it's appearances
emojisRaw = '''
CrySmile 😂 U+1F602
LoudCry 😭
Cry 😢
SmileSmile 😊
Fire 🔥
ThumbsUp 👍
Heart ❤ \ufe0f \u2764
Coffee ☕ \u2615
'''

emojiDict = dict()
for line in emojisRaw.split('\n'):
	if line.isspace() or line == "":
		continue
	emojiName = line.split()[0]
	emojiSymbol = line.split()[1]
	emojiDict[emojiName] = emojiSymbol


def ask(*question):
	# question = ' '.join([str(q) for q in question])
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
