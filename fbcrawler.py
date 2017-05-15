from bs4 import BeautifulSoup
from urlparse import urlparse
import unicodecsv as csv 
import datetime
import requests
import logging
import pickle
import facepy
import sqlite3
import json 
import sys
import os
import re

logging.basicConfig(filename='errors.log',level=logging.DEBUG)

class Post:
	def __init__(self, data):
		# we can differntiate between a post that was started in GN4 or in WordPress: interesting angle for analysis?
		self.text = None
		self.id = None
		self.link = None
		self.creator = None
		self.type = None
		self.insight = False
		
		# time stuff
		self.timestamp = datetime.datetime.strptime(data['created_time'], '%Y-%m-%dT%H:%M:%S+0000')
		self.c_time = self.timestamp.isoformat()
		self.week_day = self.timestamp.weekday()
		self.mod_time = datetime.datetime.now()

		# meta
		self.id = data['id']
		self.type = data['type']

		if data.has_key('admin_creator'):
			self.creator = data['admin_creator']['name']

		# link not always present
		if data.has_key('link'):
			self.link = data['link']

		if data.has_key('message'):
			self.text = data['message']
			
			# find shortener
			if re.search('https://nrch.nl/', self.text):
				match = re.search('https://nrch.nl/', self.text)
				short = self.text[match.start():match.end() + 4]
				self.link = requests.get(short).url
		
		# posts sometimes do not have a message
		if data.has_key('status_type'):
			if data['status_type'] != 'shared_story':
				if data.has_key('message'):
					self.text = data['message']

		# insight 
		self.get_insight()

		# meta
		self.get_meta()

		# save to database
		self.to_sql()

	def get_insight(self):
		metrics = ['post_impressions', 'post_consumptions', 'post_consumptions_by_type']
		output = {}

		for m in metrics: 
			data = graph.get(self.id + '/insights/' + m)

			if m == 'post_consumptions_by_type':
				try:
					output['link_click'] = data['data'][0]['values'][0]['value']['link clicks']
				except IndexError as e:
					output['link_click'] = None
					logging.warning('Error %s with %s \n %s' % (e.message, self.id, output))
				except TypeError as e:
					output['link_click'] = None
					logging.warning('Error %s with %s \n %s' % (e.message, self.id, output))
				except KeyError as e:
					output['link_click'] = None
					logging.warning('Error %s with %s \n %s' % (e.message, self.id, output))
			else:
				try:
					output[m] = data['data'][0]['values'][0]['value']
				except IndexError as e:
					output[m] = None
					logging.warning('Error %s with %s \n %s' % (e.message, self.id, output))


		self.impressions = output['post_impressions']
		self.consumptions = output['post_consumptions']
		self.clicks = output['link_click']

		shares = graph.get(self.id + '?fields=shares')

		if shares.has_key('shares'):
			self.shares = shares['shares']['count']
		else:
			self.shares = None
		
		self.insight = True	

	def get_meta(self):
		# only process nrc.nl
		parser = urlparse(self.link)

		if parser[1] != 'www.nrc.nl':
			self.title = None
			self.tags = None
			self.dossier = None
			return

		soup = BeautifulSoup(requests.get(self.link).text, 'html.parser')
		
		#title
		title = soup.find('h1', {'data-flowtype' : 'headline'})

		if title:
			self.title = title.text
		if soup.find('h1', { 'data-flowtype' : 'mondayprofile-headline' }):		
			# maandagprofiel
			title = soup.find('h1', { 'data-flowtype' : 'mondayprofile-headline' })
			self.title = title.text
		else:
			# catch all title on URL
			self.title = parser.path.split('/')[-1].split('-')[0]

		# keywords
		keywords = soup.findAll('meta', {'name':'keywords'})
		keys = [k['content'] for k in keywords][0]
		keys = keys.split(',')
		
		tags = []
		
		for k in keys:
			k = k.strip()
			if k == '':
				pass
			else:
				tags.append(k)

		if tags == []:
			self.tags = None
		elif len(tags) == 1:
			self.tags = tags[0]
		if len(tags) > 1:
			self.tags = ', '.join(tags)

		# dossier
		dossier = soup.find('h6', {'class': 'more-in-dossier__heading__headline'})

		if dossier:
			self.dossier = dossier.text
		else:
			self.dossier = None

	def to_sql(self):
		# connect db
		conn = sqlite3.connect('facebook-meta.db')
		c = conn.cursor()
		
		export = [	self.id,
					self.type,
					self.timestamp,
					self.c_time,
					self.week_day,
					self.mod_time,
					self.link,
					self.creator,
					self.text,
					self.title,
					self.dossier,
					self.tags,
					self.impressions,
					self.consumptions,
					self.shares,
					self.clicks,
			]

		c.execute("INSERT INTO facebook VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", export)

		conn.commit()

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


# if sys.argv[1] == -update check hydrated every post posted less than 24 hours ago and only crawl last day

# resuming if db
if 'facebook-meta.db' not in os.listdir('.'):
	conn = sqlite3.connect('facebook-meta.db')
	c = conn.cursor()
	c.execute('''CREATE TABLE facebook 
				(	id text,
					type text,
					time_stamp date,
					c_time timestamp,
					week_day int,
					mod_time timestamp,
					link text,
					creator text,
					message text,
					title text,
					dossier text,
					tags text,
					impressions int,
					consumptions int,
					shares int,
					clicks int
				)
			''')
	conn.commit()
	ids = []
else:
	conn = sqlite3.connect('facebook-meta.db')
	c = conn.cursor()
	c.execute('SELECT id FROM facebook')
	ids = [id[0] for id in c.fetchall()]

dates = []

while posts.has_key('paging'):
	for post in posts['data']:
		if post['id'] in ids:
			print '%s was scraped' % post['id']
			continue
		else:
			post_obj = Post(post)

		if post_obj.timestamp.date() not in dates:
			print 'Processing:', post_obj.timestamp.date()
	
		dates.append(post_obj.timestamp.date())

	posts = requests.get(posts['paging']['next']).json()	
	print '* Crawled %i posts' % len(dates)