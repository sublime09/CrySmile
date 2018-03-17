import os
from twython import Twython
import json
from pandas import DataFrame, read_pickle
from CSutils import emojiDict, ask

# ''' ########### REMEMBER: #################'''
# '''MAX Number of Search Requests within 15-min window: 450'''
# '''We will get BLACKLISTED if we abuse the Twitter API'''
# ''' The secret file is NOT PUBLIC to avoid abuse of our Twitter access'''

# default parameters for a query:
qParams = dict(count='100', lang='en', result_type='recent', tweet_mode='extended')
# max count is 100!!!!

def doQueries():
	twitter = getTwitter()
	queriesToDo = list()
	for emojiName in emojiDict:
		if len(queriesToDo) > 40:
			print("Over 40 queries; Revoking access...")
			os.remove(secretFilename)
			exit()
		else:
			if ask("Twitter query for", emojiName, "?"):
				queriesToDo.append(emojiName)

	queryResults = dict()
	for queryName in queriesToDo:
		qParams['q'] = emojiDict[queryName][0]
		jsonResult = twitter.search(**qParams)
		queryResults[queryName] = jsonResult
	return queryResults


def getTwitter():
	# reading the secrets....
	secretFilename = 'secret.txt'
	with open(secretFilename, 'r') as f:
		APP_KEY = f.readline().strip()
		APP_SECRET = f.readline().strip()
		ACCESS_TOKEN = f.readline().strip()
	twitter = Twython(APP_KEY, access_token=ACCESS_TOKEN)
	return twitter

def saveQueryResults(queryResults):
	for queryName, qJSON in queryResults.items():
		df = jsonToDataFrame(qJSON)
		filepath = 'data'+os.path.sep+queryName+'.p'

		if os.path.isfile(filepath):
			print("Saving UPDATE", filepath, "...", end='')
			oldDF = read_pickle(filepath)
			df = df.append(oldDF)
		else:
			print("Saving NEW", filepath, "...", end='')

		df.drop_duplicates(subset='id', inplace=True)
		df.to_pickle(filepath)
		print("Done!")

def jsonToDataFrame(jsonResult):
	tweetRows = jsonResult["statuses"]
	df = DataFrame.from_dict(tweetRows)

	screen_names = [r['screen_name'] for r in df['user']]
	goodCols = ['id', 'full_text']

	df = df[goodCols]
	df.insert(1, 'screen_name', screen_names, True)

	return df
