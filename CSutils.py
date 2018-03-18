from twython import Twython

# This is the name of an emoji followed by all of it's appearances
emojisRaw = '''
CrySmile 😂
Heart ❤ \ufe0f \u2764
Coffee ☕ \u2615
'''

emojiList = emojisRaw.split('\n')
while '' in emojiList:
	emojiList.remove('')

emojiDict = dict()

for line in emojiList:
	line = line.strip().split(" ")
	if len(line) == 0:
		continue
	keyName = line[0]
	valuesList = line[1:]
	emojiDict[keyName] = valuesList


def ask(*question):
	question = ' '.join([str(q) for q in question])
	print(question)
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