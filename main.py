#!/usr/bin/python
# -*- coding: utf-8 -*-
# old shit, haven't had time to clean up this shit, will do when i have the time ... such spaghetti
from pprint import pprint
import jsonpickle
import requests
import urllib
import re
import os

#deletes scrape.sh, if there is one already
os.path.exists("scrape.sh") and os.remove("scrape.sh")

cli_id = "02gUJC0hH2ct1EGOcYXQIzRFU91c72Ea"
artist = [ ]
sscrape = "soundscrape -f -n 100 "

# request the id for the username.
def get_sc_uid(username):
	requid = requests.get('http://api.soundcloud.com/resolve.json?url=http://soundcloud.com/%s&client_id=%s' % (username, cli_id), stream=True)
	uid = requid.text.replace(',', '').replace('kind', '').replace('"', '')
	uinfo = uid.split(":")
	
	return uinfo[1]
# request all data about the people 'x' follows
def follower_scrape():
	url =  'https://api.soundcloud.com/users/%s/followings?client_id=%s&limit=1000&offset=0' % (get_sc_uid("bendyr"), cli_id)
	spoon = urllib.urlopen(url)
	
	# dumps everything into a json object.
	jsonjar = jsonpickle.encode(spoon)
	
	# if you want to see all the crap comming out from soundcloud api
	#print jsonjar

	# regex expression to find all permalinks.
	find_permalink = re.compile(ur'"permalink\\":\\"[a-zA-Z0-9 ]{3,15}')
	regex_magic = re.findall(find_permalink, jsonjar)
	
	#iterates through all the of the findings from the regex, and removes some characters to only the get a artists name
	for i in regex_magic:
		artist.append(i.replace('"', "").replace('permalink', "").replace('\:', "").replace('\\', ""))
	
	# prints out all the artist, and counts them..
	pprint(artist)
	print "Count:", len(artist)

def soundscrape_generate():
	# Opens a file, makes it writable,
	file = open('scrape.sh', "wb+")
	# iterates through all the artist in the list, and then dump them to the file.
	for j in artist:
		dmp = sscrape + j
		file.write(dmp)
		file.write("\n")
		
follower_scrape()
# if you want to generate a bash script to download songs from all the artist you are following
# soundscrape_generate()
