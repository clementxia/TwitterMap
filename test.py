from elasticsearch import Elasticsearch
import certifi

es = Elasticsearch(['https://search-twittermap-vajtqvv3pewuza3q7243qj676e.us-east-1.es.amazonaws.com'])
res = es.search(
	index="index", 
	body={
		"size": 100,
		"query": {
			"match_all" : {}
		}
	}
)
print(res['hits']['total'])