from db_params import db_dbname, db_host, db_password, db_user, db_driver_name
#sqlalchemy engine setup with mysql
mysql_connect_string = '%s://%s:%s@%s/%s?charset=utf8' \
    % (db_driver_name, db_user, db_password, db_host, db_dbname)
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from models import Page, Ranks, Nevek
from collect_data import PairRankPage

#pool recycle set to 1 min
#because the pythonanywhere mysql server will close connections in a few mins
#see http://docs.sqlalchemy.org/en/rel_0_7/core/engines.html?highlight=pool_recycle
engine = create_engine(mysql_connect_string, pool_recycle=60)
# create a configured "Session" class
Session = sessionmaker(bind=engine)


#get records from table nevek with sqlalchemy
def get_nevek_from_db():
    result = engine.execute(Nevek.__table__.select())
    return result

#get records from table nevek with sqlalchemy
def get_pages_from_db():
    result = engine.execute(Page.__table__.select())
    return result

'''
search for page by url
if page does not exists, save page into db
if page already exists, update the timestamp
if page already exists, then delete child records (that is Ranks)
save list of ranks assigned to the page as child records of the page
'''
def save_page(page, ranks=None):
    session = Session()
    session.expire_on_commit = False
    #search for page by url
    page_from_db = session.query(Page).filter(Page.url == page.url).first()
    if not page_from_db:
        #if page does not exists, save page into db
        page.ts = datetime.now()
        session.add(page)
    else:
        page.id = page_from_db.id
        #if page already exists, update the timestamp
        session.query(Page).filter(Page.id == page_from_db.id).update({"ts": page.ts})
        #if page already exists, then delete child records (that is Ranks)
        session.query(Ranks).filter(Ranks.page_id == page.id).delete()
    session.flush()
    #save list of ranks assigned to the page as child records of the page
    if ranks:
        for rank in ranks:
            rank.page_id = page.id
            session.add(rank)
    session.commit()
    session.close()

'''get page and associated ranks records from the db'''
def get_ranks_from_db(url):
    ranks = None
    session = Session()
    page_from_db = session.query(Page).filter(Page.url == url).first()
    if page_from_db:
        ranks = session.query(Ranks).filter(Ranks.page_id == page_from_db.id).all()
        session.close()
    return page_from_db, ranks

'''
get page and associated ranks records from the db
if ranks does not exists in the db, scrap ranks (load url, parse the loaded webpage)
if scrap was successful, then save page and ranks to db and then reload (
(reload from db after save would not be necessary)
'''
def get_ranks_for_url(url):
    page, ranks = get_ranks_from_db(url)
    if ranks:
        return ranks
    else:
        scrapped_page = PairRankPage(url)
        scrapped_page.download_and_parse()
        if scrapped_page.is_ok():
            save_page(scrapped_page, scrapped_page.ranks)
            #page, ranks = get_ranks_from_db(url)
            #return ranks
            return scrapped_page.ranks
    return None




if __name__ == '__main__':
    #tests stub
    page1 = Page()


    print(page1)
    page1.url = 'http://url24.com'
    page1.ts = datetime.now()
    print(page1)

    rank = Ranks()
    rank.name2 = 'name2'
    rank.name1 = 'name1'
    rank.pair = 12
    rank.percentage = 3.3
    rank.rank = 3
    rank.score = 1.2345

    rank2 = Ranks()
    rank2.name2 = '2name2'
    rank2.name1 = '2name1'
    rank2.pair = 212
    rank2.percentage = 23.3
    rank2.rank = 23
    rank2.score = 21.2345

    tu = ('27', '8', '230,0', '36,9', 'Fischer Kati', 'Eipel Judit')
    '''print(tu)
    rt = RankTuple(*tu)
    print(rt)
    r = Ranks(**rt._asdict())'''
    r = Ranks.create_from_tuple(tu)
    print(r)

    save_page(page1, [rank, rank2, r])
