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
#because the pythonanywhere mysql server will close conecctions in a few mins
#see http://docs.sqlalchemy.org/en/rel_0_7/core/engines.html?highlight=pool_recycle
engine = create_engine(mysql_connect_string, pool_recycle=60)
# create a configured "Session" class
Session = sessionmaker(bind=engine)


#get records from table nevek with sqlalchemy
def get_nevek_from_db():
    result = engine.execute(Nevek.__table__.select())
    return result

def save_page(page, ranks=None):
    session = Session()
    page_from_db = session.query(Page).filter(Page.url == page.url).first()
    if not page_from_db:
        page.ts = datetime.now()
        session.add(page)
    else:
        page.id = page_from_db.id
        session.query(Page).filter(Page.id == page_from_db.id).update({"ts": page.ts})
        session.query(Ranks).filter(Ranks.page_id == page.id).delete()
    session.flush()
    if ranks:
        for rank in ranks:
            rank.page_id = page.id
            session.add(rank)
    session.commit()
    session.close()

def inner_get_ranks_from_db(url):
    result = None
    session = Session()
    page_from_db = session.query(Page).filter(Page.url == url).first()
    if page_from_db:
        result = session.query(Ranks).filter(Ranks.page_id == page_from_db.id).all()
        session.close()
    return page_from_db, result

def get_ranks_from_db(url):
    page, ranks = inner_get_ranks_from_db(url)
    if not ranks:
        scrap = PairRankPage(url)
        if scrap.is_ok():
            save_page(scrap, scrap.records)
            page, ranks = inner_get_ranks_from_db(url)
    return ranks



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
