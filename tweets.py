import tweepy
import boto3

auth = tweepy.OAuthHandler('AWW6rTRWBxN5e5wLexfPgTAjk', 'mD4jgCivPTUELeb1ndM42MQd2GintKxCzxjtAkZqCwdHHXth3K')
auth.set_access_token('761691441680769024-uuv60bDwcWJbh9VYMgC29yRhsdNmhNU', 'IGIsqIvatvxQtkdODvlXLsIWZCD1c2TZfvxdwjdFpcShA')

api = tweepy.API(auth)
sqs = boto3.resource('sqs', region_name='us-west-2')
queue = sqs.get_queue_by_name(QueueName='tweets')
print(queue.url)

class MyStreamListener(tweepy.StreamListener):
	def on_status(self, status):
		if status.lang != 'en' or status.coordinates == None:
			return
		global queue
		queue.send_message(MessageBody=status.text, MessageAttributes={
			'Longitude': {
				'StringValue': str(status.coordinates['coordinates'][0]),
				'DataType': 'Number'
			},
			'Latitude': {
				'StringValue': str(status.coordinates['coordinates'][1]),
				'DataType': 'Number'
			}
		})
		print(status.coordinates['coordinates'])

myStreamListener = MyStreamListener()
myStream = tweepy.Stream(auth = api.auth, listener = myStreamListener)
myStream.filter(track=['java', 'news', 'and', 'cloud'])
