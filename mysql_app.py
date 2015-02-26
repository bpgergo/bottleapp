db_host = 'localhost'
db_user = 'mi6app'
db_password = 'mi6app'
db_port = 5433
db_dbname = 'drop_me'

from bottle import route, default_app, run, template

#import mysql package for raw SQL
import MySQLdb
#get records from table nevek
#no connection pooling, new connection is created for each query
def get_raw_sql(sql):
    conn = MySQLdb.connect(host=db_host, user=db_user,
        passwd=db_password, db=db_dbname, charset='utf8')
    cur = conn.cursor()
    cur.execute(sql)
    res = cur.fetchall()
    cur.close()
    conn.close()
    return res

@route('/nevek-raw')
def nevek_raw():
    return template('nevek-tuple', nevek=get_raw_sql("SELECT * FROM nevek"))

#this will be imported and run by the wsgi.py (in hosted env)
application = default_app()

#this will be used when running on your own machine
if __name__ == '__main__':
    run(application)
