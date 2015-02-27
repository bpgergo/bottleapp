from lxml import html
import requests
import re
from models import Ranks, Page
from datetime import datetime


class PairRankPage(Page):

    '''
    Extra data from line of text into a tuple using regexp
    example input:
       1    15  300,1    69,5  Mezei Katalin - Sebes Gabor
    returns:
    ('1', '15', '300,1', '69,5', 'Mezei Katalin', 'Sebes Gabor')
    '''
    def get_pair_rank_tuple(self, line):
        m = re.match('(\d+)\s+(\d+)\s+([0-9,]+)[ *]+([0-9,]+)\s+(.*) - (.*)', line.strip())
        if m:
            return m.groups()
        return None

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
        #get records from the <PRE> tag that contains plain text in the follwoing form
        content = tree.xpath('//pre/text()')
        if content:
            self.ranks = [Ranks.create_from_tuple(item) for item in
                filter(bool, map(self.get_pair_rank_tuple, content[0].split('\r\n')))]

    def is_ok(self):
        return bool(self.url) and bool(self.ts) and bool(self.ranks)

    def __init__(self, url):
        self.url = url
        self.ranks = None

if __name__ == '__main__':
    def get_url(url):
        parsed = PairRankPage(url)
        parsed.download_and_parse()
        print(parsed.url)
        print(parsed.ts)
        for i in parsed.ranks:
            print(i)
        return parsed
    p = get_url('http://palatinusbridge.hu/mezhon/eredmenyek/2015palaered/csutortok/pc150101.htm')
        #get_url('http://palatinusbridge.hu/mezhon/eredmenyek/2015palaered/csutortok/pc150122.htm')
    print(p)