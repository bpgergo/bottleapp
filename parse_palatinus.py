# -*- coding: utf-8 -*-
from lxml import html
import requests
import re
from models import Ranks, Page
from datetime import datetime
from collections import namedtuple
import logging

#helper class, more like a struct in C, defined by name and fields
RankTuple = namedtuple('RankTuple', 'rank, pair, score, percentage, names')
RankTupleTie = namedtuple('RankTupleTie', 'rank, pair, score, percentage, tie, names')

'''
download and parse pages like these:
 http://palatinusbridge.hu/mezhon/eredmenyek/2013palaered/vasarnap/pv131215.htm
 http://palatinusbridge.hu/mezhon/eredmenyek/2015palaered/csutortok/pc150122.htm
'''
class ParsePage(Page):

    '''
    Extract data from line of text into a tuple using regexp
    example inputs:
       1    15  300,1    69,5  Mezei Katalin - Sebes Gabor
       1     3  195,0 *  62,5  2    Bozzai Péter - Albrecht Károly
       8    11  157,1 *  50,3       Ember László - Spielmann János - Hegedűs László
    returns: Rank instance
    '''
    def convert_line_to_rank(self, line):
        logging.debug('converting line:%s' % line)
        #this pattern matches lines that contain tie column
        m_with_tie = re.match('(\d+)\s+(\d+)\s+([0-9,]+)[ *]+([0-9,]+)\s+([0-9,]+)\s+(.+)', line.strip())
        result = None
        rank_tuple = None
        if m_with_tie:
            rank_tuple = RankTupleTie(*m_with_tie.groups())
        else:
            #this pattern matches lines that does not contain tie column
            m = re.match('(\d+)\s+(\d+)\s+([0-9,]+)[ *]+([0-9,]+)\s+(.+)', line.strip())
            if m:
                rank_tuple = RankTuple(*m.groups())
        if rank_tuple:
            result = Ranks()
            result.rank = rank_tuple.rank
            result.pair = rank_tuple.pair
            logging.debug('names:%s' % rank_tuple.names)
            names = rank_tuple.names.split(' - ')
            if len(names) > 0:
                result.original_name1 = names[0].strip()
            if len(names) > 1:
                result.original_name2 = names[1].strip()
            if len(names) > 2:
                result.original_name3 = names[2].strip()
            result.score = rank_tuple.score.replace(',', '.')
            result.percentage = rank_tuple.percentage.replace(',', '.')
            try:
                result.tie = rank_tuple.tie
            except AttributeError:
                result.tie = None
            logging.debug('parsed:%s' % result)
        return result

    '''
    example:
    http://palatinusbridge.hu/mezhon/eredmenyek/2015palaered/csutortok/pc150122.htm
    '''
    def download_and_parse(self):
        #load url
        page = requests.get(self.url)
        #parse html
        tree = html.fromstring(page.text)
        #get date from <HEAD><TITLE>2015-01-22 &nbsp;Pala csutortok 2015.01.22</TITLE>
        title = tree.xpath('//head/title/text()')
        if title:
            date = title[0].split(' ')
            if date:
                try:
                    self.ts = datetime.strptime(date[0], '%Y-%m-%d')
                except ValueError:
                    self.ts = None
        #get records from the <PRE> tag that contains plain text in the following form
        content = tree.xpath('//pre/text()')
        #logging.debug(content)
        line_end = '\r\n'
        if line_end not in content:
            line_end = '\n'
        if content:
            self.ranks = list(filter(bool, map(self.convert_line_to_rank, content[0].split(line_end))))

    def is_ok(self):
        return bool(self.url) and bool(self.ts) and bool(self.ranks)

    def __init__(self, crawl_id, url):
        self.crawl_id = crawl_id
        self.url = url
        self.ranks = []

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    def get_url(url):
        parsed = ParsePage(url)
        #line = '    1     3     31  64,6  Fürst Panni - Zalai Mari       '
        #converted = parsed.convert_line_to_rank(line)
        #logging.debug(converted)
        parsed.download_and_parse()
        return parsed
    p = get_url('http://palatinusbridge.hu/mezhon/eredmenyek/2013palaered/vasarnap/pv131215.htm')
        #'http://palatinusbridge.hu/mezhon/eredmenyek/2015palaered/szombat/pz150117.htm')
        #'http://palatinusbridge.hu/mezhon/eredmenyek/2015palaered/csutortok/pc150101.htm')
        #get_url('http://palatinusbridge.hu/mezhon/eredmenyek/2015palaered/csutortok/pc150122.htm')
    logging.debug(p)