import QueryTwitter
import EmojiFrame as EF
from EmojiFrame import EmojiFrame
import Clustering

	# ''' ########### REMEMBER: #################'''
# '''MAX Number of Search Requests within 15-min window: 450'''
# '''We will get BLACKLISTED if we abuse the Twitter API'''
# ''' The secret file is NOT PUBLIC to avoid abuse of our Twitter access by attackers'''

def main():
	QueryTwitter.main()
	EF.main()
	Clustering.main()


if __name__ == '__main__':
	main()
	