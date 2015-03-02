from db_params import db_dbname, db_host, db_password, db_user, db_driver_name
#sqlalchemy engine setup with mysql
mysql_connect_string = '%s://%s:%s@%s/%s?charset=utf8' \
    % (db_driver_name, db_user, db_password, db_host, db_dbname)
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from models import Page, Ranks, Nevek, Alias
from parse_palatinus import ParsePage
from name_util import clean_name, weak_vowel_shorten #, match_levenshtein
import logging
from sqlalchemy.exc import IntegrityError
from difflib import get_close_matches

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

def get_alias_from_db():
    result = engine.execute(Alias.__table__.select())
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
        scrapped_page = ParsePage(url)
        scrapped_page.download_and_parse()
        if scrapped_page.is_ok():
            save_page(scrapped_page, scrapped_page.ranks)
            #page, ranks = get_ranks_from_db(url)
            #return ranks
            return scrapped_page.ranks
    return None



def populate_names_from_ranks():
    session = Session()
    for rank in session.query(Ranks).all():
        rec = Nevek()
        rec.name = clean_name(rank.name1)
        logging.debug('saving %s' % rec.name)
        try:
            session.add(rec)
            session.flush()
            session.commit()
        except IntegrityError:
            logging.debug('already exists %s' % rec.name)
            session.rollback()

def get_names_for_matching():
    session = Session()
    return set([nevek.name for nevek in session.query(Nevek).all()])


def save_alias(alias, name, generator):
    session = Session()
    rec = Alias()
    rec.alias = alias
    rec.name = name
    rec.generator = generator
    logging.debug(rec)
    logging.debug('saving... %s' % rec)
    try:
        session.add(rec)
        session.flush()
        session.commit()
    except IntegrityError:
        logging.debug('already exists %s' % rec)
        session.rollback()


def generate_aliases_difflib():
    names = get_names_for_matching()
    for name in names:
        matches = get_close_matches(name, names, n=3, cutoff=0.8)
        if matches:
            for match in matches:
                if match != name and match[0] == name[0]:
                    save_alias(match, name, 'difflib')
'''
def generate_aliases_levenshtein():
    names = get_names()
    for name in names:
        for other_name in names:
            if name != other_name and match_levenshtein(name, other_name):
                save_alias(other_name, name, 'levenshtein')
'''

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    logging.info(datetime.now())
    #populate_names_from_ranks()
    #logging.info(datetime.now())
    #generate_aliases_levenshtein()
    #logging.info(datetime.now())
    generate_aliases_difflib()
    logging.info(datetime.now())

