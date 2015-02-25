db_host = 'localhost'
db_user = 'mi6app'
db_password = 'mi6app'
db_port = 5433
db_dbname = 'drop_me'

import postgresql

from bottle import route, default_app, run, template
db = postgresql.open('pq://%s:%s@%s:%i/%s' % (db_user, db_password, db_host, db_port, db_dbname))

def get_sql(sql):
    return db.query(sql)

@route('/nevek')
def nevek():
    return template('nevek-tuple', nevek=get_sql("SELECT * FROM nevek"))

#this will be imported and run by the wsgi.py (in hosted env)
application = default_app()

#this will be used when running on your own machine
if __name__ == '__main__':
    run(application)
