import datetime
import requests
import pickle
import facepy
import json 

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


def auth():
	""" auth works with a local pickle file with the access token, if access token expires, script prompts user with new input from cli """
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

# crawl untill date?
while len(database) < 1000:
	
	for post in posts['data']:
		database.append(Post(post))

	posts = requests.get(posts['paging']['next']).json()

# build mysql database perhaps?
with open('fb-posts.p', 'wb') as pickle_out:
	pickle.dump(posts)

