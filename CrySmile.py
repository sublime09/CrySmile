from CSutils import ask
import QueryTwitter
import Preprocess


if ask("Query Twitter?"):
	results = QueryTwitter.doQueries()
	QueryTwitter.saveQueryResults(results)

if ask("Preprocess?"):
	Preprocess.processDataFrames()
	# do preprocessing...

