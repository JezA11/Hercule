import shodan
import sys
import favicon
import mmh3
import requests
import codecs
import csv

# Configuration
API_KEY = "MWJcH9qmAIuIrrzuihnXGQ18Mc0cYz3x"

# Input validation
if len(sys.argv) == 1:
        print('Usage: %s <search query>' % sys.argv[0])
        sys.exit(1)

print("====================================================================")

try: #create results file
    f = open("searchResults.csv",'w') 
    csvwriter = csv.writer(f)

except Exception as e: #file system issues
        print('Error: %s' % e)
        sys.exit(1)

try:
    # Setup the api
    api = shodan.Shodan(API_KEY)

    #write header row to csv file
    csvwriter.writerow(["hostnames","ip","ip_str","os","port","timestamp"]) 

    # Search for favicons at given url
    icons = favicon.get(sys.argv[1])
    print ("Grabbed {} icons from {}".format(len(icons),sys.argv[1]))
    
    for icon in icons:
        # Grab favicons and hash
        iconResponse = requests.get(icon[0]) 
        hash = mmh3.hash(codecs.encode(iconResponse.content,"base64"))

        # Perform the search
        query = 'http.favicon.hash:' + str(hash) #build query
        result = api.search(query) #run query

        # Loop through the matches for each favicon hash and print results to stdout and file
        for service in result['matches']:
                csvwriter.writerow([service['hostnames'], service['ip'], service['ip_str'], service['os'], service['port'], service['timestamp']]) #writes data to csv file
                print("===========================")
                print(service['ip_str'])
                print("https://www.shodan.io/host/{}".format(service['ip_str'])) #prints url of shodan host page
                print(query)
                print(service['hostnames'])
    f.close()

except Exception as e: #connection issues
        print('Error: %s' % e)
        sys.exit(1)