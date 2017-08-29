import re
import httplib
import urllib2
from urlparse import urlparse
from HTMLParser import HTMLParser
 
class MyHTMLParser(HTMLParser):
 
    def handle_starttag(self, tag, attrs):
        # Only parse the 'anchor' tag.
        if tag == "a":
           # Check the list of defined attributes.
           for name, value in attrs:
               # If href is defined, print it.
               if name == "href":
                   print name, "=", value
 
regex = re.compile(
       r'^(?:http|ftp)s?://' # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
        r'localhost|' #localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
        r'(?::\d+)?' # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
 
def isValidUrl(url):
    if regex.match(url) is not None:
        return True;
    return False
 
def crawler(SeedUrl):
    tocrawl = [SeedUrl]
    crawled = []
    while tocrawl:
        page = tocrawl.pop()
        print('Pop!')
        try:
            print('Opening page...' + page)
            pagesource = urllib2.urlopen(page)
            print('Reading...')
            s = pagesource.read()
            parser = MyHTMLParser()
            parser.feed(s)
            print 'Crawled: ' + page + ' -- Status Code: ' + str(pagesource.getcode())
            links = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', s)
            print(links)
            if page not in crawled:
                for i in range(len(links)):
                    if isValidUrl(links[i]):
                        print('Valid URL')
                        tocrawl.append(links[i])
        except urllib2.HTTPError, err:
            print "ERROR: " + page + ' -- Status Code: ' + str(pagesource.getcode())
        except urllib2.URLError, err:
            print "Some other error happened:", err.reason
        except Exception, exc:
            print exc
        print('Still crawling...')
        crawled.append(page)
    return crawled
crawler('https://google.com')