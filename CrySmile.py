# ''' REMEMBER: '''
# '''MAX Number of Search Requests within 15-min window: 450'''
# '''We will get BLACKLISTED if we abuse the Twitter API'''

def readFile(filename):
	lines = list()
	with open(filename, 'r') as f:
		for line in f:
			lines.append(line.strip())
	return lines
		
secrets = readFile('secret.txt')
APP_KEY = secrets[0]
APP_SECRET = secrets[1]
ACCESS_TOKEN = secrets[2]

callCounter = 0

print("APP is setting up!")
from twython import Twython
twitter = Twython(APP_KEY, access_token=ACCESS_TOKEN)

def getResults(params):
	if callCounter > 400:
		print("CallCounter is over 400; quitting...")
		sleep(3)
		return
	if callCounter % 50 == 0:
		response = input("CallCounter is at", callCounter, ", continue?")
		if response.lower() not in ['y', 'yes']:
			return
	results = twitter.search(params)
	return results

# hashtags = "sarcasm".split(" ")
# terms = """\s""".split(" ")

queries = "#sarcasm \s".split(" ")
print("Queries = ", queries)
exit()

params = dict()
params["count"] = 20 #max is 100
params["result_type"] = 'recent'
params["lang"] = 'en'

dataset = []

for q in queries:
	params['q'] = q
	results = getResults(params)
	for r in results:
		searchResults = r['statuses']
		tweetText = searchResults['text']
		tweetTime = r['']
		# row = dict(query=q, text=tweetText, time=)

	# tweet = results[]


fullresults = set()

results = getResults(params)

for r in results:
	print(r)
