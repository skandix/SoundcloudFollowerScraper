#!/usr/bin/python
from sys import platform as _os
import argparse
import requests
import sys
import os
import re

# global vars
osEnd = ""
os.path.exists("scrape"+osEnd) and os.remove("scrape"+osEnd)
artist = [ ]
sscrape = "soundscrape -f -n 50"


def get_sc_uid(username):
    scrapeid = requests.get("https://soundcloud.com/"+username).text
    return  map(lambda x: x.replace("soundcloud:users:", ""), re.findall(u'soundcloud:users:\d+', scrapeid))[0]

def follower_scrape(cli_id):
    try:
        fScrape = requests.get('https://api.soundcloud.com/users/{:}/followings?client_id={:}&limit=1000&offset=0'.format(get_sc_uid(args.username), cli_id)).json()
        for j in fScrape['collection']:
            artist.append(j['permalink'])

    except ValueError as valerr:
        if not cli_id:
            print ("Error: API Key is missing/wrong")
            sys.exit(1)

        else:
            print ("Error: {:} \n ").format(valerr)
            sys.exit(1)
    
    except TypeError as e:
        return # fix this later, now it's time to sleep again..

    print (artist)
    print (len(artist))

def soundscrape_generate():	
    with  open('scrape'+osEnd, "w+") as file:
        for j in artist:
            dmp = sscrape +" "+ j
            file.write(dmp)
	    file.write("\n")

if _os == "linux" or _os == "linux2" or _os == "cygwin" or _os == "darwin":
    osEnd = ".sh"

elif _os == "win32":
    osEnd = ".bat"

parser = argparse.ArgumentParser()
parser.add_argument("--username", type=str)
parser.add_argument("--api", type=str)
args = parser.parse_args()

follower_scrape(args.api)
soundscrape_generate()

