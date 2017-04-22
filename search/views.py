from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader
from dwebsocket import accept_websocket
import elasticsearch
from django.views.decorators.csrf import csrf_exempt
import json
import urllib2

es = elasticsearch.Elasticsearch('https://search-tweets-utlvp5kqwhmiafxmczczhpcqku.us-east-1.es.amazonaws.com')

# Create your views here.
@csrf_exempt 
def index(request):
	return render(request, 'search/index.html')

@accept_websocket
def echo(request):
	for message in request.websocket:
		message = '111'
		request.websocket.send(message)
	#return HttpResponse('111')

@csrf_exempt
def collect(request):
	if request.method == 'POST':
		type = request.META.get('HTTP_X_AMZ_SNS_MESSAGE_TYPE')
		if type == 'SubscriptionConfirmation':
			json_data = json.loads(request.body)
			url = json_data['SubscribeURL']
			urllib2.urlopen(url).read()
			return HttpResponse('Subscribe Successful!')
		if type == 'Notification':
			json_data = json.loads(request.body)
			text = json_data['Message']
			es.index(index='tweets',doc_type='test_type', body=text)
			render(request, 'search/index.html')
			return HttpResponse(status=200)
	return HttpResponse('Unknown')

def search(request, keyword):
	#key = request.GET.get('search')
	response = locate(keyword)
	print(keyword)
	hr = HttpResponse(json.dumps(response))
	hr["Access-Control-Allow-Origin"] = "*"
	hr["Access-Control-Allow-Method"] = "GET"
	hr["Access-Control-MAX-AGE"] = "1000"
	hr["Access-Control-Allow-Headers"] = "*"
	return hr
	#return HttpResponse(json.dumps(response))

def locate(keyword):
	#es = Elasticsearch(['https://search-twittermap-vajtqvv3pewuza3q7243qj676e.us-east-1.es.amazonaws.com'])
	res = es.search(
		index="tweets", 
		body={
			"size": 500,
			"query": {
				"match" : {
					"text" : keyword
				}
			}
		}
	)
	response = []
	for doc in res['hits']['hits']:
		#location = doc['_source']['coordinates']['coordinates']
		lat = doc['_source']['latitude']
		lon = doc['_source']['longitude']
		text = doc['_source']['text']
		sentiment = doc['_source']['sentiment']
		response.append({'lat': lat, 'lon': lon, 'text':text, 'sentiment':sentiment})

	return response