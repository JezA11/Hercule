import favicon
import mmh3
import requests
import sys
import csv
import codecs

#get favicons from friendly URL
friendlyIcons = favicon.get(sys.argv[1])
friendlyIconHashes = []


#calculate mmh3 hash of each icon and append to list
for icon in friendlyIcons:
    iconResponse = requests.get(icon[0])
    friendlyIconHashes.append(mmh3.hash(codecs.encode(iconResponse.content,"base64")))
print("Grabbed {} favicons".format(len(friendlyIconHashes)))

#open phish tank csv, create csv object, and skip header row
try:
    f = open(sys.argv[2])
    csvFile = csv.reader(f)
    next(csvFile)

except Exception as e: #filesystem errors
    print('Error: %s' % e)
    sys.exit(1)

rowCount = sum(1 for row in csvFile) #gets number of records in file
f.seek(0) # return to first record after counting rows

phishes = []
pagesSeen = 0 # seen == line read
pagesChecked = 0 # checked == targets match so pull favicons
failedConnections = 0 # Usually 404 or 503 if phish page has already been removed
for webPage in csvFile:
    #if sys.argv[3] in webPage[7]: #for speed - don't make web requests if target as listed in phishtank is not "our" page
    pagesChecked += 1
    try:
        phishIcons = favicon.get(webPage[1]) #get favicons from phish page url
        for icon in phishIcons: #for each favicon from phishing page
            iconResponse = requests.get(icon[0])
            phishIconHash = mmh3.hash(codecs.encode(iconResponse.content,"base64")) #calculate icon hash
            if phishIconHash in friendlyIconHashes: #if matches a friendly icon...
                phishes.append(webPage) # ...phish caught! Add to list
    except Exception as e: #usually due to 404 or 503
        failedConnections += 1
        #print('Error: %s' % e) # suppressed for brevity
    pagesSeen += 1
    if pagesSeen % 1000 == 0: # prints progress every 1000 rows. There's probably a better way of doing this
        print("{}/{} ({}%) complete. {} suspicious pages.".format(pagesSeen,rowCount,format(((pagesSeen/rowCount)*100),'.2f'), len(phishes)))
    
f.close() #close file



# Print results summary
print("============================================================")
print("Found {} phishing pages related to {}.".format(len(phishes), sys.argv[1]))
print("Checked {}/{} pages. {} failed connections.".format(pagesChecked, pagesSeen, failedConnections))
print("============================================================")


#print url of suspicious pages
print("Suspicious pages:")
for page in phishes:
    print("------------------------------------------------------------")
    print(page[1])
    
    