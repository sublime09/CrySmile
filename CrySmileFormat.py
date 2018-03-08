import os
import json
from pandas import DataFrame
import pandas

emojiDict = dict(CrySmile="😂")

print("Formatting JSON...")

for emojiName, emoji in emojiDict.items():
	filename = emojiName+".json"
	with open(filename) as data_file:
		data = json.load(data_file)
		data = data["statuses"]
		data = DataFrame.from_dict(data)
		# print(data)

		print(data["text"])

		# for key in data:
		# 	print(key)


print("Formatting done!")

	# print(pandaResult)
	### TODO: start formatting the search results
	# for r in searchResults:
	# 	print(r)
		# searchResults = r['statuse	s']
		# tweetText = searchResults['text']
		# tweetTime = r['']
		# row = dict(query=q, text=tweetText, time=)
		### TODO: add to full dataset, probably a pandas datafrmae
