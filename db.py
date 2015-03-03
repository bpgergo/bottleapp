# -*- coding: utf-8 -*-
from db_params import db_dbname, db_host, db_password, db_user, db_driver_name
#sqlalchemy engine setup with mysql
mysql_connect_string = '%s://%s:%s@%s/%s?charset=utf8' \
    % (db_driver_name, db_user, db_password, db_host, db_dbname)
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from models import Crawl, Page, Ranks, Nevek, Alias
from parse_palatinus import ParsePage
from name_util import clean_name, weak_vowel_shorten #, match_levenshtein
import logging
from sqlalchemy.exc import IntegrityError
from difflib import get_close_matches
from sqlalchemy import or_

#pool recycle set to 1 min
#because the pythonanywhere mysql server will close connections in a few mins
#see http://docs.sqlalchemy.org/en/rel_0_7/core/engines.html?highlight=pool_recycle
engine = create_engine(mysql_connect_string, pool_recycle=60)
# create a configured "Session" class
Session = sessionmaker(bind=engine)


#get records from table nevek with sqlalchemy
def get_nevek_from_db():
    result = engine.execute(Nevek.__table__.select().order_by(Nevek.name))
    return result

def get_alias_from_db():
    result = engine.execute(Alias.__table__.select().order_by(Alias.name))
    return result

#get records from table nevek with sqlalchemy
def get_pages_from_db():
    result = engine.execute(Page.__table__.select())
    return result

def get_crawls_from_db():
    return engine.execute(Crawl.__table__.select())

def get_pages_for_crawl_url(url):
    session = Session()
    pages = []
    crawl = session.query(Crawl).filter(Crawl.url == url).first()
    if crawl:
        pages = session.query(Page).filter(Page.crawl_id == crawl.id).all()
    #session.close()
    return pages

def save_crawl(url):
    remove_crawl(url)
    session = Session()
    crawl = Crawl(url = url, ts = datetime.now())
    session.add(crawl)
    session.commit()
    crawl_id = crawl.id
    session.close()
    return crawl_id

def remove_crawl(url):
    session = Session()
    #search for page by url, delete existing data
    crawl = session.query(Crawl).filter(Crawl.url == url).first()

    if crawl:
        logging.info('deleting existing crawl id:%s', crawl.id)
        for page in session.query(Page).filter(Page.crawl_id == crawl.id):
            remove_page(page.url)
        session.query(Crawl).filter(Crawl.id == crawl.id).delete()
        session.flush()
        session.commit()
    session.close()


def remove_page(url):
    session = Session()
    #search for page by url, delete existing data
    page_from_db = session.query(Page).filter(Page.url == url).first()
    if page_from_db:
        logging.info('deleting existing page and ranks records by page.id:%s', page_from_db.id)
        session.query(Ranks).filter(Ranks.page_id == page_from_db.id).delete()
        session.query(Page).filter(Page.id == page_from_db.id).delete()
        session.flush()
        session.commit()
    session.close()


'''
search for page by url
if page does not exists, save page into db
if page already exists, update the timestamp
if page already exists, then delete child records (that is Ranks)
save list of ranks assigned to the page as child records of the page
'''
def save_page(page):
    session = Session()
    page.ts = datetime.now()
    logging.info('about to insert new page:%s', page)
    session.add(page)
    session.flush()
    logging.info('inserted page:%s', page)
    session.commit()
    result = page.id
    session.close()
    return result


def save_ranks(ranks):
    session = Session()
    for r in ranks:
        logging.info('about to insert new rank:%s', r)
        session.add(r)
        session.flush()
        logging.info('inserted rank:%s', r)
    session.commit()
    session.close()

'''get page and associated ranks records from the db'''
def get_page_and_ranks_from_db(url):
    ranks = None
    session = Session()
    page_from_db = session.query(Page).filter(Page.url == url).first()
    if page_from_db:
        ranks = session.query(Ranks).filter(Ranks.page_id == page_from_db.id).all()
        session.close()
    return page_from_db, ranks

'''
scrap ranks (load url, parse the loaded webpage)
if scrap was successful, then save page and ranks to db and then reload (
'''
def save_ranks_for_url(crawl_id, url):
    scrapped_page = ParsePage(crawl_id, url)
    scrapped_page.download_and_parse()
    if scrapped_page.is_ok():
        logging.debug('url downloaded and parsed:%s', url)
        remove_page(url)
        save_page(scrapped_page)



'''
get page and associated ranks records from the db
if ranks does not exists in the db, scrap ranks (load url, parse the loaded webpage)
if scrap was successful, then save page and ranks to db and then reload (
(reload from db after save would not be necessary)
'''
def get_ranks_for_url(url):
    session = Session()
    ranks = []
    page = session.query(Page).filter(Page.url == url).first()
    if page:
        ranks = session.query(Ranks).filter(Ranks.page_id == page.id).all()
    #session.close()
    return ranks


def add_name(name, session=Session()):
    if name:
        rec = Nevek()
        rec.name = clean_name(name)
        logging.debug('saving %s' % rec.name)
        try:
            session.add(rec)
            session.flush()
            session.commit()
        except IntegrityError:
            logging.debug('already exists %s' % rec.name)
            session.rollback()


def populate_names_from_rank(rank, session):
    add_name(rank.original_name1, session)
    add_name(rank.original_name2, session)
    add_name(rank.original_name3, session)


def populate_names_for_page(page, session):
    for rank in session.query(Ranks).filter(Ranks.page_id == page.id).all():
        populate_names_from_rank(rank, session)

def populate_names_from_all_ranks():
    session = Session()
    for rank in session.query(Ranks).all():
        populate_names_from_rank(rank, session)
    session.close()


def get_names_for_matching():
    session = Session()
    return set([nevek.name for nevek in session.query(Nevek).all()])


def inner_save_alias(alias, session):
    logging.debug('saving alias... %s' % alias)
    try:
        session.add(alias)
        session.commit()
    except IntegrityError:
        logging.debug('already exists %s' % alias)
        session.rollback()


def merge_alias(alias, match, session):
    if match != alias.name and match != alias.alias1 and match != alias.alias2 and match != alias.alias3 \
        and match != alias.alias4 and match != alias.alias5:
        if not alias.alias2:
            alias.alias2 = match
        elif not alias.alias3:
            alias.alias3 = match
        elif not alias.alias4:
            alias.alias4 = match
        elif not alias.alias5:
            alias.alias5 = match
        session.commit()

def save_alias(name, matches, generator, session):
    new = True
    alias = find_alias(name, session, generator)
    if alias:
        new = False
        for match in matches:
            merge_alias(alias, match, session)

    else:
        for match in matches:
            alias = find_alias(name, session, generator)
            if alias:
                new = False
                merge_alias(alias, match, session)

    if new:
        rec = Alias()
        rec.name = name
        rec.generator = generator
        rec.alias1 = matches[0]
        if len(matches) > 1:
            rec.alias2 = matches[1]
        if len(matches) > 2:
            rec.alias3 = matches[2]
        if len(matches) > 3:
            rec.alias4 = matches[3]
        if len(matches) > 4:
            rec.alias5 = matches[4]
        inner_save_alias(rec, session)


def get_nevek_by_name(name, session=Session()):
    return session.query(Nevek).filter(Nevek.name == name).first()


def find_alias(name, session=Session(), generator='difflib'):
    return session.query(Alias).filter(or_(Alias.name == name, Alias.alias1 == name,
            Alias.alias2 == name, Alias.alias3 == name, Alias.alias4 == name, Alias.alias5 == name))\
        .filter(Alias.generator==generator).first()

'''
update rank with unified names
'''
def update_rank_with_aliases(rank, session=Session(), generator='difflib'):
    logging.debug("update rank with aliases start:%s", rank)
    change = False
    sql = '''select id, name from alias
        where (name='%s' or alias1='%s' or alias2='%s' or alias3='%s' or alias4='%s' or alias5='%s')
        and generator = '%s'
        order by alias limit 1;
        '''
    alias = find_alias(rank.original_name1, session, generator)
    if alias:
        logging.debug("alias 1:%s", alias.name)
        name_rec = get_nevek_by_name(alias.name, session)
        logging.debug("nevek 1:%s", name_rec)
        if name_rec:
            rank.name1_id = name_rec.id
            change = True
    alias = find_alias(rank.original_name2, session, generator)
    if alias:
        logging.debug("alias 2:%s", alias.name)
        name_rec = get_nevek_by_name(alias.name, session)
        logging.debug("nevek 2:%s", name_rec)
        if name_rec:
            rank.name2_id = name_rec.id
            change = True
    if rank.original_name3:
        alias = find_alias(rank.original_name3, session, generator)
        if alias:
            logging.debug("alias 3:%s", alias.name)
            name_rec = get_nevek_by_name(alias.name, session)
            logging.debug("nevek 3:%s", name_rec)
            if name_rec:
                rank.name3_id = name_rec.id
                change = True
    if change:
        logging.debug("update rank with values:%s",
            str({"name1_id": rank.name1_id, "name2_id": rank.name2_id, "name3_id": rank.name3_id}))
        session.query(Ranks).filter(Ranks.id == rank.id).update({
            "name1_id": rank.name1_id, "name2_id": rank.name2_id, "name3_id": rank.name3_id})
        session.commit()

def generate_alias_for_name(name, names, session):
    matches = get_close_matches(name, names, n=6, cutoff=0.85)
    #match list always contains the name itself, remove it!
    matches = list(filter(lambda x: x != name, matches))
    #rule from experience: remove those matches that start with different char
    matches = list(filter(lambda x: x[0] == name[0], matches))
    if matches:
        logging.debug("match found for name:%s; matches:%s" % (name, matches))
        save_alias(name, sorted(matches), 'difflib', session)


def generate_aliases_for_page(page, session):
    names = get_names_for_matching()
    for rank in session.query(Ranks).filter(Ranks.page_id == page.id).all():
        if rank.original_name1:
            generate_alias_for_name(rank.original_name1, names, session)
        if rank.original_name1:
            generate_alias_for_name(rank.original_name1, names, session)
        if rank.original_name1:
            generate_alias_for_name(rank.original_name1, names, session)

def generate_all_aliases():
    session = Session()
    names = get_names_for_matching()
    for name in names:
        generate_alias_for_name(name, names, session)
    session.commit()
    session.close()

def update_ranks_with_aliases(ranks, session, generator='difflib'):
    for rank in ranks:
        update_rank_with_aliases(rank, session, generator)


def disambiguation_page(page, session):
    logging.debug('%s : start collecting names' % (datetime.now()))
    populate_names_for_page(page, session)
    session.commit()
    logging.debug('%s : start generating aliases' % (datetime.now()))
    generate_aliases_for_page(page, session)
    session.commit()
    logging.debug('%s : start updating ranks with aliases' % (datetime.now()))
    session.commit()
    update_ranks_with_aliases(session.query(Ranks).filter(Ranks.page_id == page.id) .all(), session, 'difflib')

def disambiguation_url(url):
    session = Session()
    crawl = session.query(Crawl).filter(Crawl.url == url).first()
    for page in session.query(Page).filter(Page.crawl_id == crawl.id).all():
        disambiguation_page(page, session)
    session.close()
    logging.debug('%s : finished processing ' % (datetime.now()))


def disambiguation_all():
    logging.debug('%s : start collecting names' % (datetime.now()))
    populate_names_from_all_ranks()
    logging.debug('%s : start generating aliases' % (datetime.now()))
    generate_all_aliases()
    logging.debug('%s : start updating ranks with aliases' % (datetime.now()))
    session = Session()
    update_ranks_with_aliases(session.query(Ranks).all(), session, 'difflib')
    session.commit()
    session.close()
    logging.debug('%s : finished processing ' % (datetime.now()))



'''
def generate_aliases_levenshtein():
    names = get_names()
    for name in names:
        for other_name in names:
            if name != other_name and match_levenshtein(name, other_name):
                save_alias(other_name, name, 'levenshtein')
'''



def test_save_page():
    url = 'http://hello.tessek.co.uk'
    remove_page(url)
    page = Page()
    page.url = url
    ranks = []
    rank = Ranks()
    rank.original_name1 = 'Hey Joe'
    rank.original_name2 = 'Hall Hello'
    rank.rank = 5
    rank.pair = 6
    rank.score = 1.2
    rank.percentage = 5.5
    ranks.append(rank)
    rank = Ranks()
    rank.original_name1 = 'Hey Joe2'
    rank.original_name2 = 'Hall Hello2'
    rank.rank = 52
    rank.pair = 62
    rank.score = 21.2
    rank.percentage = 25.5
    ranks.append(rank)
    page.ranks = ranks
    save_page(page)

def test_update_rank_with_aliases():
    session = Session()
    rank = session.query(Ranks).filter(Ranks.id == 4176).first()
    logging.debug(rank)
    update_rank_with_aliases(rank, session)
    session.close()



if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    logging.info(datetime.now())
    update_ranks_with_aliases('difflib')
    logging.info(datetime.now())

