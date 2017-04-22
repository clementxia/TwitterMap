import multiprocessing
import time
import boto3
import json
from watson_developer_cloud import NaturalLanguageUnderstandingV1
import watson_developer_cloud.natural_language_understanding.features.v1 as \
features

nlu = NaturalLanguageUnderstandingV1(
    version='2017-02-27',
    username='7660b1cb-3fec-42fb-9833-2be72b5a2b72',
    password='vBWy4EK3o1jB')

def sqs_poll():
	sqs = boto3.resource('sqs')
	sns = boto3.client('sns')
	queue = sqs.get_queue_by_name(QueueName='tweets')
	while True:
		message = queue.receive_messages(
			MessageAttributeNames=['All']
		)
		if len(message) == 0:
			time.sleep(5)
		else:
			if message[0].message_attributes is not None:
				message_send = {}
				text = message[0].body
				try:
					response = nlu.analyze(text=message[0].body, features=[features.Sentiment()])
				except:
					print("error")
					message[0].delete()
				else:
					sentiment = response['sentiment']['document']['label']
					longitude = message[0].message_attributes.get('Longitude').get('StringValue')
					latitude = message[0].message_attributes.get('Latitude').get('StringValue')
					message_send['text'] = text
					message_send['longitude'] = longitude
					message_send['latitude'] = latitude
					message_send['sentiment'] = sentiment
					json_data = json.dumps(message_send)
					sns.publish(Message=json_data, TopicArn='arn:aws:sns:us-west-2:181604895085:tweets')
					message[0].delete()


num_processes = range(1, 5)
for num in num_processes:
	p = multiprocessing.Process(target=sqs_poll)
	p.start()