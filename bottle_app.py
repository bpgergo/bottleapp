#web framework imports
from bottle import default_app, route, run, template, redirect, request
from db import get_nevek_from_db, get_ranks_from_db

#basic handler will redirect to nevek
@route('/')
def hello_world():
    redirect('/nevek')

@route('/nevek')
def nevek():
    return template('nevek-obj', nevek=get_nevek_from_db())

@route('/ranks')
def ranks():
    url = request.query.get('url')
    print("url:"+url)
    res = template('ranks-obj', ranks=get_ranks_from_db(url))

    return res


#this will be imported and run by the wsgi.py (in hosted env)
application = default_app()

#this will be used when running on your own machine
if __name__ == '__main__':
    run(application, debug=True)
