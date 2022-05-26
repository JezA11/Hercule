# Hercule
A python-tool for hunting phishing webpages using Internet-wide scanning technologies.


========================================================================================
shodanQuery.py

For automated grabbing of favicons from a specified "friendly" webpage. 
Favicons are hashed and used as a search operator to identify phishing webpages using stolen resources.
Creates "searchResults.csv" in local directory.

Must add API key to .py file before use.

Usage:

$ python shodanQuery.py [url including protocol]
eg
$ python shodanQuery.py https://www.paypal.com/us/home

========================================================================================
censysQuery.py

Usage as above, but far less effective. Not recommended due to api limits (Maximum 200 requests per month).
Query runs without issue but favicon md5 hash but never returns results in either API or web portal. 

Must add API keys to .py file before use.

$ python censysQuery.py [url including protocol]
eg
$ python censysQuery.py https://www.paypal.com/us/home

========================================================================================
QueryRepo.py

For testing of favicon matching as a phishing page detection tool. 
Uses Phish Tank's phishing webpage repository, released hourly. Download from http://data.phishtank.com/data/online-valid.csv
"Target org" must be exact match as found in Phish Tank CSV. This allows script to skip phishing pages which target a different organisation, for efficiency.
For example, in a repo of ~8000 pages, typically only ~100 will explicitly target Microsoft

Usage:

$ python queryRepo.py [url including protocol] [path to repository csv] [target org]
eg
$ python queryRepo.py https://www.microsoft.com/en-us/ verified_online.csv Microsoft
