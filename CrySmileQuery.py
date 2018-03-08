import os
from twython import Twython
import json
# import pandas as pd

# ''' REMEMBER: '''
# '''MAX Number of Search Requests within 15-min window: 450'''
# '''We will get BLACKLISTED if we abuse the Twitter API'''
# ''' The secret file is NOT available to public to avoid abuse of our Twitter access'''

# reading the secrets....
secretFilename = 'secret.txt'
with open(secretFilename, 'r') as f:
	APP_KEY = f.readline().strip()
	APP_SECRET = f.readline().strip()
	ACCESS_TOKEN = f.readline().strip()
		
# default parameters for a query:
# max count is 100!!!!
qParams = dict(count='100', lang='en', result_type='mixed', tweet_mode='extended')

emojiDict = dict(CrySmile=["😂"], Heart=["❤", '\ufe0f', '\u2764'])


queries = emojiDict

# def queryAndSave(queries, key, token):
twitter = Twython(APP_KEY, access_token=ACCESS_TOKEN)
queryCount = 0
for queryName, query in queries.items():
	if queryCount > 40:
		print("QueryCount is over 40; Revoking access...")
		os.remove(secretFilename)
		exit()
	else:
		print("Do you want to Twitter search this:", queryName, "?")
		answer = input("Answer yes or no:\n")
		if answer.strip().lower() == "yes":
			qParams['q'] = query[0]
			jsonResult = twitter.search(**qParams)
			queryCount += 1
			with open(queryName+".json", 'w') as outfile:
			    json.dump(jsonResult, outfile)
			    print("Searched and saved as JSON:", queryName)
		else:
			print("NOT Searched:", queryName)
