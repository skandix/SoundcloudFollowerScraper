#!/usr/bin/python
import requests
import os

os.path.exists("scrape.sh") and os.remove("scrape.sh")

cli_id = "02gUJC0hH2ct1EGOcYXQIzRFU91c72Ea"
artist = [ ]
sscrape = "soundscrape -f -n 100 "

def get_sc_uid(username):
	requid = requests.get('http://api.soundcloud.com/resolve.json?url=http://soundcloud.com/{:s}&client_id={:s}'.format(username, cli_id)).json()
	return requid['id']

def follower_scrape():
	fScrape = requests.get('https://api.soundcloud.com/users/{:}/followings?client_id={:}&limit=1000&offset=0'.format(get_sc_uid("bendyr"), cli_id)).json()
	
	for j in fScrape['collection']:
		artist.append(j['permalink'])

	print artist
	print len(artist)

def soundscrape_generate():
	
	file = open('scrape.sh', "wb+")
	
	for j in artist:
		dmp = sscrape + j
		file.write(dmp)
		file.write("\n")
		
follower_scrape()
soundscrape_generate()
