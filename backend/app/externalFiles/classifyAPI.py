'''
Example input:
python classifyAPI.py isbn 080906233X
'''


import sys, http.server, urllib.request, urllib.parse, urllib.error, urllib.parse, xml.dom.pulldom, xml.dom.minidom, cgi, socket, xml.sax.saxutils, io, string, codecs, time, datetime, os
from urllib.parse import urlencode

if len(sys.argv) > 2:
	parmType = sys.argv[1] # isbn
	parmValue = sys.argv[2] # 080906233X
	summaryInd = 'false' 
	'''
	return top book result rather than all "editions"
	"false" returns FAST Subject Headings
	IN THIS CASE: don't use "true" since we want the headings
	'''
	if len(sys.argv) > 3: summaryInd = sys.argv[3]
else:
	print('Usage: python classifySample.py <param-type> <param-value> [true]')
	print('For example: python classifySample.py isbn 0679442723 true')
	sys.exit(1)
 
print('Sample Python Client for Classify 2')
print('Searching for: ' + parmType + '=' + parmValue)

base = 'http://classify.oclc.org/classify2/Classify?'
summaryBase = '&summary=true'

def getText(nodelist):
    rc = ""
    for node in nodelist:
        if node.nodeType == node.TEXT_NODE:
            rc = rc + node.data
    return rc

xdoc = ''
try:
	if summaryInd == 'true': nextURL = base + urlencode({parmType:parmValue.encode('utf-8')}) + summaryBase
	else: nextURL = base + urlencode({parmType:parmValue.encode('utf-8')})
	print(nextURL) # XML: send this to front end	
	urlobj = urllib.request.urlopen(nextURL)
	response = urlobj.read()
	urlobj.close()		
	xdoc = xml.dom.minidom.parseString(response)
except UnicodeDecodeError:
	print('UnicodeDecodeError: ' + nextURL)
except IOError:
	print('IOError: ' + nextURL)

response = xdoc.getElementsByTagName('response')[0]
respCode = response.attributes["code"].value
print('Method response: ' + respCode)

# ISBN input results in one book, then print this:
if respCode == '0' or respCode == '2':
	recommendations = xdoc.getElementsByTagName('recommendations')[0]
	if recommendations:
		if len(xdoc.getElementsByTagName('ddc')) > 0:
			ddc = recommendations.getElementsByTagName('ddc')[0]
			if ddc:
				for mostPopular in ddc.getElementsByTagName('mostPopular'):
					holdings = mostPopular.attributes["holdings"].value
					nsfa = mostPopular.attributes["nsfa"].value
					sfa = mostPopular.attributes["sfa"].value
					print('DDC mostPopular: class=' + sfa + ' normalized=' + nsfa + ' holdings=' + holdings)
		
		if len(xdoc.getElementsByTagName('lcc')) > 0:
			lcc = recommendations.getElementsByTagName('lcc')[0]
			if lcc:
				for mostPopular in lcc.getElementsByTagName('mostPopular'):
					holdings = mostPopular.attributes["holdings"].value
					nsfa = mostPopular.attributes["nsfa"].value
					sfa = mostPopular.attributes["sfa"].value
					print('LCC mostPopular: class=' + sfa + ' normalized=' + nsfa + ' holdings=' + holdings)

# Multiple books returned from an ISBN input, print info for those books
# Then use the "owi" number to search again, replacing the ISBN number
elif respCode == '4':
	works = xdoc.getElementsByTagName('works')[0]
	print('Works found: ' + str(len(works.getElementsByTagName('work'))))
	
	for work in works.getElementsByTagName('work'):
		author = work.attributes["author"].value
		title = work.attributes["title"].value
		editionCount = work.attributes["editions"].value
		date = work.attributes["lyr"].value
		format = work.attributes["format"].value
		owi = work.attributes["owi"].value
		print('title=' + title + ' author=' + author + ' editions=' + editionCount + ' format=' + format + ' owi=' + owi + ' date=' + date)