
import os

from twisted.web import http, proxy
from twisted.internet import reactor

import logging

logging.basicConfig(level=logging.DEBUG)

mario = open('mario.gif').read()


class ProxyClient(proxy.ProxyClient):
    """Mange returned header, content here.

    Use `self.father` methods to modify request directly.
    """

    contentType = "unknown"
    index = 0

    def handleHeader(self, key, value):
        # change response header here
        if key.lower() == 'content-type':
            self.contentType = value
        if key.lower() == 'content-length':
            # bypass it
            return
        proxy.ProxyClient.handleHeader(self, key, value)

    def handleResponsePart(self, buffer):
        # change response part here
        # make all content upper case
        if self.contentType in ('image/gif', 'image/png', 'image/jpeg', 'image/jpg'):
            buffer = mario
        if 'html' in self.contentType:
            buffer = self.mangleHtml(buffer)
        if 'css' in self.contentType:
            buffer = self.mangleHtml(buffer)
        if 'image' in self.contentType and False:
            type = self.contentType.split('/')[1]
            ProxyClient.index += 1
            img = self.mangleImage(buffer, ProxyClient.index, type)
        proxy.ProxyClient.handleResponsePart(self, buffer)

    def mangleHtml(self, html):
        # Let's hope the html is mangleable
        html = html.replace('background:', 'notbackground:')
        html = html.replace('background-color:', 'notbackground:')
        html = html.replace('<body', '<body style="background-color:pink !important" ')
        return html

    def mangleImage(self, buffer, index, type):
        fn = '{0}.{1}'.format(index, type)
        print fn
        open(fn, 'w').write(buffer)
        os.system("convert {0} -colorize 0,50,50 {0}".format(fn))
        return open(fn, 'rb').read()


class ProxyClientFactory(proxy.ProxyClientFactory):
    protocol = ProxyClient


class ProxyRequest(proxy.ProxyRequest):
    protocols = dict(http=ProxyClientFactory)

    def process(self):
        self.requestHeaders.removeHeader('accept-encoding')
        #print self.uri
        #import pprint
        #pprint.pprint(self.requestHeaders)
        return proxy.ProxyRequest.process(self)


class Proxy(proxy.Proxy):
    requestFactory = ProxyRequest


class ProxyFactory(http.HTTPFactory):
    protocol = Proxy

if __name__ == '__main__':
    reactor.listenTCP(8080, ProxyFactory())
    reactor.run()
