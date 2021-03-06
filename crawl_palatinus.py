from pattern.web import Crawler, DEPTH, HTMLLinkParser, FIFO
from db import save_crawl, save_ranks_for_url
from re import match
import logging

'''
crawl these pages: http://palatinusbridge.hu/mezhon/eredmenyek/
'''
class Palatinus(Crawler):
    def __init__(self, links=[], domains=[], delay=20.0, parse=HTMLLinkParser().parse, sort=FIFO):
        #call super constructor
        Crawler.__init__(self, links, domains, delay, parse, sort)
        #save first link into root_url attribute
        self.root_url = links[0]
        self.crawl_id = save_crawl(self.root_url)
        # this will match on the end of rank urls like
        # http://palatinusbridge.hu/mezhon/eredmenyek/2014palaered/hetfo/ph140120.htm
        self.target_pattern = 'p\w\d{6}\.htm'
        # this will match on the end of day urls like
        # http://palatinusbridge.hu/mezhon/eredmenyek/2014palaered/hetfo/
        self.day_pattern = '[a-z]{4,9}/\Z'
        self.year_pattern = '[0-9]{4}palaered/\Z'


    #rule that filters interesting pages
    def follow(self, link):
        result = False
        logging.debug('checking pattern:%s' % link.referrer + self.target_pattern)
        if match(link.referrer + self.target_pattern, link.url):
            logging.debug('target found:%s', link.url)
            save_ranks_for_url(self.crawl_id, link.url)

        logging.debug('checking pattern:%s' % link.referrer + self.day_pattern)
        if match(link.referrer + self.day_pattern, link.url):
            logging.debug('will follow link:%s, from:%s', repr(link.url), link.referrer)
            result = True

        logging.debug('checking pattern:%s' % link.referrer + self.day_pattern)
        if match(link.referrer + self.year_pattern, link.url):
            logging.debug('will follow link:%s, from:%s', repr(link.url), link.referrer)
            result = True

        return result

def crawl_url(url):
    logging.info('crawling url:%s', url)
    p = Palatinus(links=[url], delay=2)
    while not p.done:
        p.crawl(method=DEPTH, cached=False, throttle=1)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    crawl_url('http://palatinusbridge.hu/mezhon/eredmenyek/')
