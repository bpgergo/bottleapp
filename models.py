from collections import namedtuple
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()
from sqlalchemy import Column, ForeignKey, \
    Integer, String, Float, SmallInteger, DateTime
#from sqlalchemy.orm import relationship, backref


#sqlalchemy model class for table 'nevek'
class Nevek(Base):
    __tablename__ = 'nevek'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    lev = Column(SmallInteger)
    point = Column(Float)
    play = Column(Integer)
    kmp = Column(Float)


class Page(Base):
    __tablename__ = 'page'
    id = Column(Integer, primary_key=True, autoincrement=True)
    url = Column(String(250), nullable=False, unique=True)
    ts = Column(DateTime, nullable=False)
    #ranks = relationship("Ranks", order_by="Ranks.id", backref="page")

    def __repr__(self):
        return "<Page(id=%s, url='%s', ts=%s)>" % (
            self.id, self.url, str(self.ts))

#helper class, more like a struct in C, defined by name and fields
RankTuple = namedtuple('RankTuple', 'rank, pair, score, percentage, name1, name2')


class Ranks(Base):
    __tablename__ = 'ranks'
    id = Column(Integer, primary_key=True, autoincrement=True)
    page_id = Column(Integer, ForeignKey('page.id'), primary_key=True)
    rank = Column(Integer, nullable=False)
    pair = Column(Integer, nullable=False)
    score = Column(Float, nullable=False)
    percentage = Column(Float, nullable=False)
    name1 = Column(String(250), nullable=False)
    name2 = Column(String(250), nullable=False)
    #page = relationship("Page", backref=backref('page', order_by=id))

    @classmethod
    def create_from_tuple(self, tup):
        rank_tup = RankTuple(*tup)
        #Ranks(**RankTuple(*tup))
        result = Ranks()
        result.rank = rank_tup.rank
        result.pair = rank_tup.pair
        result.name1 = rank_tup.name1
        result.name2 = rank_tup.name2
        result.score = rank_tup.score.replace(',', '.')
        result.percentage = rank_tup.percentage.replace(',', '.')
        return result

    def __repr__(self):
        return "<Rank(id=%s, page_id=%s, name1='%s', name2='%s', score=%s, percentage=%s)>" % (
            self.id, self.page_id, self.name1, self.name2, self.score, self.percentage)


if __name__ == '__main__':
    pass