import unicodecsv as csv
import datetime
import requests
import pickle
import facepy
import json 
import os

class Post:
	def __init__(self, data):
		self.admin_creator = data['admin_creator']
		self.timestamp = datetime.datetime.strptime(data['created_time'], '%Y-%m-%dT%H:%M:%S+0000')
		self.text = data['message']
		self.link = data['link']
		self.id = data['id']
		self.type = data['type']

	def get_insight(self):
		metrics = ['post_impressions', 'post_consumptions', 'post_consumptions_by_type']
		output = {}

		for m in metrics:
			data = graph.get(self.id + '/insights/' + m)
			if m == 'post_consumptions_by_type':
				output['link_click'] = data['data'][0]['values'][0]['value']['link clicks']
			else:
				output[m] = data['data'][0]['values'][0]['value']

		# dynamically update class attributes when added to metrics list
		self.impressions = output['post_impressions']
		self.consumptions = output['post_consumptions']
		self.clicks = output['link_click']

	def to_file(self):
		# check for keys, or process what to write to csv as arg

		if 'output.csv' not in os.listdir('.'):
			with open('output.csv', 'w') as csv_out:
				writer = csv.writer(csv_out, delimiter='\t')
				writer.writerow(['Article', 'Impressions', 'Consumptions', 'Clicks'])	
		else:
			out = [self.link, self.impressions, self.consumptions, self.clicks]
		
			with open('output.csv', 'a') as csv_out:
				writer = csv.writer(csv_out, delimiter='\t')
				writer.writerow(out)

def getToken():
	token = raw_input('Token expired. Enter new token\nGet one here: https://developers.facebook.com/tools/explorer/\n> ')
	pickle.dump(token, open('token.p', 'wb'))
	return token

def auth():
	""" auth works with a local pickle file with the access token, if access token expires, script prompts user with new input from cli """
	print 'Authenticating with Facebook...\n'

	try:
		token = pickle.load(open('token.p', 'rb'))
	except IOError:
		token = getToken()

	if token:
		try:
			graph = facepy.GraphAPI(token)
			profile = graph.get('nrc')
		except facepy.exceptions.OAuthError:
			token = getToken()

	return facepy.GraphAPI(token)

graph = auth()
profile = graph.get('nrc')
posts = graph.get(profile['id'] + '/posts')

database = []

while posts['paging'].has_key('next'):
	
	for post in posts['data']:
		database.append(Post(post))

	posts = requests.get(posts['paging']['next']).json()
	print 'Crawled %i posts' % len(database)
	
	# implement append to database instead of rewrite
	with open('database.p', 'wb') as pickle_out:
		pickle.dump(database, pickle_out)