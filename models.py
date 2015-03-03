from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()
from sqlalchemy import Column, ForeignKey, \
    Integer, String, Float, SmallInteger, DateTime, Boolean
from sqlalchemy.orm import relationship, backref


#sqlalchemy model class for table 'nevek'
class Nevek(Base):
    __tablename__ = 'nevek'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    lev = Column(SmallInteger)
    point = Column(Float)
    play = Column(Integer)
    kmp = Column(Float)
    def __repr__(self):
        return self.name
        #return "<Nev(name=%s, point=%s)>" % (
        #    self.name, self.point)


#sqlalchemy model class for table 'alias'
class Alias(Base):
    __tablename__ = 'alias'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(250), nullable=False)
    alias1 = Column(String(250), nullable=False)
    alias2 = Column(String(250))
    alias3 = Column(String(250))
    alias4 = Column(String(250))
    alias5 = Column(String(250))
    generator = Column(String(250))
    approved = Column(Boolean)

    def __repr__(self):
        return "<Alias(name=%s, alias1='%s', alias2='%s', alias3='%s', alias4='%s', alias5='%s', generator=%s)>" % (
            self.name, self.alias1, self.alias2, self.alias3, self.alias4, self.alias5, self.generator)


class Crawl(Base):
    __tablename__ = 'crawl'
    id = Column(Integer, primary_key=True, autoincrement=True)
    url = Column(String(250), nullable=False, unique=True)
    ts = Column(DateTime, nullable=False)

    def __repr__(self):
        type_of_ranks = 'None'
        if self.ranks:
            type_of_ranks = str(type(self.ranks[0]))
        return "<Crawl(id=%s, url='%s', ts=%s>" % (
            self.id, self.url, str(self.ts))


class Page(Base):
    __tablename__ = 'page'
    id = Column(Integer, primary_key=True, autoincrement=True)
    crawl_id = Column(Integer, ForeignKey('crawl.id'), nullable=False)
    url = Column(String(250), nullable=False, unique=True)
    ts = Column(DateTime, nullable=False)
    crawl = relationship("Crawl", foreign_keys=crawl_id, lazy='subquery',
        single_parent=True, backref=backref("pages"), enable_typechecks=False)


    def __repr__(self):
        type_of_ranks = 'None'
        if self.ranks:
            type_of_ranks = str(type(self.ranks[0]))
        return "<Page(id=%s, url='%s', ts=%s, num of ranks=%s)>" % (
            self.id, self.url, str(self.ts), str(len(self.ranks)))



class Ranks(Base):
    __tablename__ = 'ranks'
    id = Column(Integer, primary_key=True, autoincrement=True)
    page_id = Column(Integer, ForeignKey('page.id'), nullable=False)
    rank = Column(Integer, nullable=False)
    pair = Column(Integer, nullable=False)
    score = Column(Float, nullable=False)
    percentage = Column(Float, nullable=False)
    tie = Column(Integer)
    original_name1 = Column(String(250), nullable=False)
    original_name2 = Column(String(250))
    original_name3 = Column(String(250))
    name1_id = Column(Integer, ForeignKey('nevek.id'))
    name2_id = Column(Integer, ForeignKey('nevek.id'))
    name3_id = Column(Integer, ForeignKey('nevek.id'))
    page = relationship("Page", foreign_keys=page_id, lazy='subquery',
                        single_parent=True, backref=backref("ranks"), enable_typechecks=False)
    name1 = relationship("Nevek", foreign_keys=name1_id, lazy='subquery', cascade=False)
    name2 = relationship("Nevek", foreign_keys=name2_id, lazy='subquery', cascade=False)
    name3 = relationship("Nevek", foreign_keys=name3_id, lazy='subquery', cascade=False)

    def __repr__(self):
        return "<Rank(id=%s, page_id=%s, name1='%s', name2='%s', name3='%s', score=%s, percentage=%s, rank=%s, tie='%s')>" % (
            self.id, self.page_id, self.original_name1, self.original_name2, self.original_name3, self.score, self.percentage, self.rank, self.tie)


if __name__ == '__main__':
    pass