#web framework imports
from bottle import default_app, route, run, template, redirect, request
from db import get_nevek_from_db, get_ranks_for_url, get_pages_from_db

#basic handler will redirect to pages
@route('/')
def redirect():
    redirect('/pages')

@route('/nevek')
def nevek():
    return template('nevek-obj', nevek=get_nevek_from_db())

@route('/pages')
def pages():
    return template('pages-obj', pages=get_pages_from_db())


@route('/ranks')
def ranks():
    url = request.query.get('url')
    res = template('ranks-obj', ranks=get_ranks_for_url(url))
    return res


#this will be imported and run by the wsgi.py (in hosted env)
application = default_app()

#this will be used when running on your own machine
if __name__ == '__main__':
    run(application, debug=True)
