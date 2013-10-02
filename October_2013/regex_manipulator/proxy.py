from twisted.web import proxy, http
from twisted.internet import reactor

from twisted.python import log
from twisted.web import http, proxy

import re

import BeautifulSoup

class ProxyClient(proxy.ProxyClient):
    """Mange returned header, content here.

    Use `self.father` methods to modify request directly.
    """
    def handleHeader(self, key, value):
        # change response header here
        log.msg("Header: %s: %s" % (key, value))
        proxy.ProxyClient.handleHeader(self, key, value)

    def handleResponsePart(self, buffer):
    	#print "Buffer : %s" % buffer
    	proxy.ProxyClient.handleResponsePart(self, buffer)

    def rawDataReceived(self, data):
		soup = BeautifulSoup.BeautifulSoup(data)
		if hasattr(soup, 'html'):
			# If we find html do some processing, otherwise assume its another file type and just pass it through.
			print "Found some html, meddling ..."
			'''h1 = soup.findAll('h1')
			for h in h1:
				h.replaceWith("<h1>%s</h1>" % h.string[::-1])

			data = soup
			print data
			'''
			insensitive_head = re.compile(re.escape('</body>'), re.IGNORECASE)
			data = insensitive_head.sub('<p>Wibble</p></body>', data )

			insensitive_head = re.compile(re.escape('<h1>'), re.IGNORECASE)
			data = insensitive_head.sub('<h1 style="color:#FF00FF;">', data )
			
			insensitive_head = re.compile(re.escape('</p>'), re.IGNORECASE)
			data = insensitive_head.sub('wibble </p>', data )			
		else:
			# not html content, just return it as normal.
			pass

		proxy.ProxyClient.rawDataReceived(self, data)

class ProxyClientFactory(proxy.ProxyClientFactory):
    protocol = ProxyClient

class ProxyRequest(proxy.ProxyRequest):
    protocols = dict(http=ProxyClientFactory)

class Proxy(proxy.Proxy):
    requestFactory = ProxyRequest

class ProxyFactory(http.HTTPFactory):
    protocol = Proxy

reactor.listenTCP(8080, ProxyFactory(), interface='0.0.0.0')
reactor.run()
