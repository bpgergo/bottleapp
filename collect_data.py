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
    def parse_pair_rank_page(self, url):
        #load url
        page = requests.get(url)
        #parse html
        tree = html.fromstring(page.text)
        #get date from <HEAD><TITLE>2015-01-22 &nbsp;Pala csutortok 2015.01.22</TITLE>
        self.ts = datetime.strptime(tree.xpath('//head/title/text()')[0].split(' ')[0], '%Y-%m-%d')
        #get records from the <PRE> tag that contains plain text in the follwoing form
        self.records = [Ranks.create_from_tuple(item) for item in
            filter(bool, map(self.get_pair_rank_tuple, tree.xpath('//pre/text()')[0].split('\r\n')))]

    def is_ok(self):
        return bool(self.url) and bool(self.ts) and bool(self.records)

    def __init__(self, url):
        self.url = url
        self.records = None
        self.parse_pair_rank_page(url)

if __name__ == '__main__':
    def get_url(url):
        parsed = PairRankPage(url)
        print(parsed.url)
        print(parsed.ts)
        for i in parsed.records:
            print(i)
        return parsed
    p = get_url('http://palatinusbridge.hu/mezhon/eredmenyek/2015palaered/csutortok/pc150122.htm')
    print(p)