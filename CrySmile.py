import time
from CSutils import ask, emojiDict
from QueryTwitter import QueryTwitter
import Preprocess

# ''' ########### REMEMBER: #################'''
# '''MAX Number of Search Requests within 15-min window: 450'''
# '''We will get BLACKLISTED if we abuse the Twitter API'''
# ''' The secret file is NOT PUBLIC to avoid abuse of our Twitter access'''


def doQueryProcess(processTime=3600):
	maxQsecRate = (180 / 15.0) / 60.0
	totalQueries = int(maxQsecRate * processTime)
	sleepSeconds = processTime / float(totalQueries)
	emojiNames = list(emojiDict.keys())

	if ask("Do", totalQueries, "queries over", processTime, "seconds?"):
		for qNum in range(totalQueries):
			emojiNum = qNum % len(emojiNames)
			emojiName = emojiNames[emojiNum]
			emojiSearchTerm = emojiDict[emojiName][0]
			query = QueryTwitter(emojiName, emojiSearchTerm)
			query.doQuery()
			query.saveDataFrame()
			time.sleep(sleepSeconds)
		print("finished!!!!!")
	else:
		print("Cancelled")



if __name__ == '__main__':
	queryTime = int(input("Enter seconds of query process:"))
	doQueryProcess(queryTime)



# if ask("Query Twitter?"):
# 	results = QueryTwitter.doQueries()
# 	QueryTwitter.saveQueryResults(results)

# if ask("Preprocess?"):
# 	Preprocess.processDataFrames()

