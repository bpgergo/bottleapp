from pattern.web import Crawler, DEPTH, HTMLLinkParser, FIFO
from db import get_ranks_for_url
from re import match
import logging

class Palatinus(Crawler):
    def __init__(self, links=[], domains=[], delay=20.0, parse=HTMLLinkParser().parse, sort=FIFO):
        #call super constructor
        Crawler.__init__(self, links, domains, delay, parse, sort)
        #save first link into root_url attribute
        self.root_url = links[0]
        # this will match on the end of rank urls like
        # http://palatinusbridge.hu/mezhon/eredmenyek/2014palaered/hetfo/ph140120.htm
        self.target_pattern = 'p\w\d{6}\.htm'
        # this will match on the end of day urls like
        # http://palatinusbridge.hu/mezhon/eredmenyek/2014palaered/hetfo/
        self.day_pattern = '[a-z]{4,9}/\Z'

    '''def visit(self, link, source=None):
        if match(link.referrer+self.target_pattern, link.url):
            logging.info('saved to db:%s', repr(link.url))
            get_ranks_for_url(link.url)'''


    #rule that filters interesting pages
    def follow(self, link):
        result = False
        logging.debug('checking pattern:%s' % link.referrer + self.target_pattern)
        if match(link.referrer + self.target_pattern, link.url):
            logging.debug('target found')
            get_ranks_for_url(link.url)

        logging.debug('checking pattern:%s' % self.root_url + self.day_pattern)
        if match(self.root_url + self.day_pattern, link.url):
            logging.debug('will follow link:%s, from:%s', repr(link.url), link.referrer)
            result = True

        return result


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    root_url = 'http://palatinusbridge.hu/mezhon/eredmenyek/2014palaered/'
    logging.info('crawling root url:%s', root_url)
    p = Palatinus(links=[root_url], delay=2)
    while not p.done:
        p.crawl(method=DEPTH, cached=False, throttle=1)