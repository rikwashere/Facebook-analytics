from bs4 import BeautifulSoup
import requests
import sys

def getKeywords(url):
	soup = BeautifulSoup(requests.get(url).text, 'html.parser')

	title = soup.h1.get_text()

	# keywords
	keywords = soup.findAll('meta', {'name':'keywords'})
	keys = [k['content'] for k in keywords][0]
	keys = keys.split(',')
	
	if keys == ',':
		key = None

	tags = []
	for k in keys:
		k = k.strip()
		if k == '':
			pass
		else:
			tags.append(k)


	# dossier
	dossier = soup.find('h6', {'class': 'more-in-dossier__heading__headline'}).get_text()

	return {	title : 'title',
				dossier : 'dossier',
				tags : 'tags' }



if __name__ == '__main__':
	if len(sys.argv) < 2:
		raise AttributeError('Program runs with input from cli. Please supply nrc.nl link')
	else:
		url = sys.argv[1] 
		print 'Processing %s' % url
		print getKeywords(url)
