#!/usr/bin/python
from sys import platform as _os
import requests
import os

osEnd = ""
xTracks = 50

os.path.exists("scrape"+osEnd) and os.remove("scrape"+osEnd)

cli_id = "02gUJC0hH2ct1EGOcYXQIzRFU91c72Ea"
artist = [ ]
sscrape = "soundscrape -f -n " + str(xTracks)

def get_sc_uid(username):
	requid = requests.get('http://api.soundcloud.com/resolve.json?url=http://soundcloud.com/{:s}&client_id={:s}'.format(username, cli_id)).json()
	return (requid['id'])

def follower_scrape():
	fScrape = requests.get('https://api.soundcloud.com/users/{:}/followings?client_id={:}&limit=1000&offset=0'.format(get_sc_uid("bendyr"), cli_id)).json()
	
	for j in fScrape['collection']:
		artist.append(j['permalink'])

	print (artist)
	print (len(artist))

def soundscrape_generate():
	
	file = open('scrape'+osEnd, "w+")
	
	for j in artist:
		dmp = sscrape +" "+ j
		file.write(dmp)
		file.write("\n")

if _os == "linux" or _os == "linux2" or _os == "cygwin" or _os == "darwin":
		osEnd = ".sh"

elif _os == "win32":
		osEnd = ".bat"

follower_scrape()
soundscrape_generate()
