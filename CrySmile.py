import QueryTwitter
import EmojiFrame

	# ''' ########### REMEMBER: #################'''
# '''MAX Number of Search Requests within 15-min window: 450'''
# '''We will get BLACKLISTED if we abuse the Twitter API'''
# ''' The secret file is NOT PUBLIC to avoid abuse of our Twitter access'''

def main():
	QueryTwitter.main()
	EmojiFrame.main()

	# if ask("Query Twitter?"):
	# 	results = QueryTwitter.doQueries()
	# 	QueryTwitter.saveQueryResults(results)

	# if ask("Preprocess?"):
	# 	Preprocess.processDataFrames()



if __name__ == '__main__':
	main()
	