db_host = 'localhost'
db_user = 'root'
db_password = 'gggggg'
db_dbname = 'test'

#web framework imports
from bottle import default_app, route, run, template, redirect

#sqlalchemy engine setup with mysql
mysql_connect_string = 'mysql+mysqldb://%s:%s@%s/%s?charset=utf8' % (db_user, db_password, db_host, db_dbname)
from sqlalchemy import create_engine
#recycle and timeout are mysql+hosting specific settings to avoid Lost connection... error.
#see http://stackoverflow.com/questions/28719982/how-should-i-use-sqlalchemy-session-in-bottle-app-to-avoid-lost-connection-to-m
engine = create_engine(mysql_connect_string, pool_recycle=499, pool_timeout=20)

from sqlalchemy import MetaData, Table, Column, Integer, String, Float, SmallInteger
#sqlalchemy model class for table 'nevek'
meta = MetaData()
nevek_table = Table('nevek', meta,
    Column('id', Integer, primary_key=True),
    Column('name', String(250), nullable=False),
    Column('lev', SmallInteger),
    Column('point', Float),
    Column('play', Integer),
    Column('kmp', Float)
)
#get records from table nevek with sqlalchemy
def get_nevek_from_db():
    return engine.execute(nevek_table.select())

#basic handler will redirect to nevek
@route('/')
def hello_world():
    redirect('/nevek')

@route('/nevek')
def nevek():
    return template('nevek-obj', nevek=get_nevek_from_db())

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
