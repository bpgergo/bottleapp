#web framework imports
from bottle import default_app, route, run, template, redirect, request
from db import get_nevek_from_db, get_ranks_for_url, get_pages_from_db, get_alias_from_db
from db import disambiguation
from crawl_palatinus import crawl_url
from multiprocessing import Pool
import logging
from datetime import datetime

#basic handler will redirect to new_crawl
@route('/')
def default_route():
    redirect('/controller')

@route('/nevek')
def nevek():
    return template('nevek-obj', nevek=get_nevek_from_db())

@route('/alias')
def alias():
    return template('alias-obj', aliases=get_alias_from_db())


@route('/pages')
def pages():
    return template('pages-obj', pages=get_pages_from_db())


@route('/ranks')
def ranks():
    url = request.query.get('url')
    res = template('ranks-obj', ranks=get_ranks_for_url(url))
    return res


@route('/controller', method='GET')
def new_item():
    if request.GET.get('start_crawl','').strip():
        url = request.GET.get('crawl_url', '').strip()
        process_url_async(url)
        return '<p>The new crawl task was created, ' \
            'the results should be available soon <a href=/pages>here</a></p>'
    elif request.GET.get('start_disambiguation','').strip():
        disambiguation_async()
        return '<p>Name disambiguation process has started, it may take a while...</p>'

    else:
        return template('controller.tpl')


def disambiguation(url):
    logging.debug('%s : start disambiguation names' % (datetime.now()))
    disambiguation()
    logging.debug('%s : end disambiguation aliases' % (datetime.now()))

def disambiguation_async():
    pool = Pool(1)
    urls = [None]
    pool.map_async(disambiguation, urls)

def process_url(url):
    logging.debug('%s : start crawling url:%s' % (datetime.now(), url))
    crawl_url(url)
    logging.debug('%s : end crawling url:%s' % (datetime.now(), url))

def process_url_async(url):
    pool = Pool(1)
    urls = [url]
    pool.map_async(process_url, urls)


#this will be imported and run by the wsgi.py (in hosted env)
application = default_app()

#this will be used when running on your own machine
if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    run(application, debug=True, reload=True)
