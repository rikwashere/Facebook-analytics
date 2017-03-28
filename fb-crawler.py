import dateutil.parser as dateparser
from prettytable import PrettyTable
from scraper import connectTwitter
from bs4 import BeautifulSoup
import requests.packages.urllib3
import datetime
import operator
import requests
import pickle
import facepy
import json 
import sys
import re

class Post:
	def __init__(self, dictionary):
		# Rebuild sometimes
		for k, v in dictionary.items():
			setattr(self, k, v)

	def get_insight(self):
		metrics = ['post_impressions', 'post_consumptions']
		output = {}

		for m in metrics:
			data = graph.get(self.id + '/insights/' + m)
			output[m] = data['data'][0]['values'][0]['value']
			
		self.impressions = output['post_impressions']
		self.consumptions = output['post_consumptions']


	# rebuild auth handshake
def auth():
	print 'Authenticating with Facebook...\n'

	try:
		token = pickle.load(open('token.p', 'rb'))
	except IOError:
		token = raw_input('No token found. Enter new token\nGet one here: https://developers.facebook.com/tools/explorer/\n> ')
		pickle.dump(token, open('token.p', 'wb'))


	if token:
		try:
			graph = facepy.GraphAPI(token)
			profile = graph.get('nrc')
		except facepy.exceptions.OAuthError:
			token = raw_input('Token expired. Enter new token\nGet one here: https://developers.facebook.com/tools/explorer/\n> ')
			pickle.dump(token, open('token.p', 'wb'))

	return facepy.GraphAPI(token)

graph = auth()

profile = graph.get('nrc')

posts = graph.get(profile['id'] + '/posts')

output = []
database = []
while len(database) < 1000:
	
	for post in posts['data']:
		database.append(Post(post))
		print post['created_time']

	posts = requests.get(posts['paging']['next']).json()

with open('fb-posts.p', 'wb') as pickle_out:
	pickle.dump(posts)

