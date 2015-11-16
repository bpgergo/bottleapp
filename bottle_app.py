#web framework imports
from bottle import default_app, route, run, template, redirect, request
from db import get_crawls_from_db, get_nevek_from_db, get_ranks_for_url, get_pages_for_crawl_url, get_alias_from_db, disambiguation_url
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


@route('/crawls')
def crawls():
    return template('crawls-obj', crawls=get_crawls_from_db())


@route('/pages')
def pages():
    url = request.query.get('url')
    return template('pages-obj', pages=get_pages_for_crawl_url(url))


@route('/ranks')
def ranks():
    url = request.query.get('url')
    res = template('ranks-obj', ranks=get_ranks_for_url(url))
    return res


@route('/controller', method='GET')
def new_item():
    if request.GET.get('start_crawl','').strip():
        url = request.GET.get('crawl_url', '').strip()
        crawl_url_async(url)
        return '<p>The new crawl task was created, ' \
            'the results should be available soon <a href=/pages?url=%s>here</a></p>' % url
    elif request.GET.get('start_disambiguation','').strip():
        url = request.GET.get('disambiguation_url', '').strip()
        disambiguation_url_async(url)
        return '<p>Name disambiguation of url has started, ' \
            'the results should be available soon <a href=/ranks?url=%s>here</a></p>' % url
    else:
        return template('controller.tpl')


def wrap_async(func, url):
    pool = Pool(1)
    urls = [url]
    pool.map_async(func, urls)


def disambiguation_url_async(url):
    wrap_async(disambiguation_url, url)


def crawl_url_async(url):
    wrap_async(crawl_url, url)

#this will be imported and run by the wsgi.py (in hosted env)
application = default_app()
logging.basicConfig(level=logging.DEBUG)

#this will be used when running on your own machine
if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    run(application, debug=True, reload=True)
    #disambiguation_url('http://palatinusbridge.hu/mezhon/eredmenyek/')
