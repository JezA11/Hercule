#!/usr/bin/env/python
#

from censys.search import CensysHosts
import hashlib
import sys
import favicon
import requests


CENSYS_API_ID="xxx"
CENSYS_API_SECRET="xxx"

# initialise API
CensysHosts(api_id=CENSYS_API_ID,api_secret=CENSYS_API_SECRET)

h = CensysHosts(api_id=CENSYS_API_ID,api_secret=CENSYS_API_SECRET)

# Input validation
if len(sys.argv) == 1:
        print('Usage: %s <search query>' % sys.argv[0])
        sys.exit(1)

# Search for favicons at given url
icons = favicon.get(sys.argv[1])
for icon in icons:
    iconResponse = requests.get(icon[0]) 
    hash2find = hashlib.md5(iconResponse.content).hexdigest() #hash favicon

    # Get search results - pages=-1 to get all results 
    for page in h.search("services.http.response.favicons.md5_hash:{}".format(hash2find), per_page=5, pages=-1):
        print(page)
