from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()
from sqlalchemy import Column, ForeignKey, \
    Integer, String, Float, SmallInteger, DateTime, Boolean
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

#sqlalchemy model class for table 'alias'
class Alias(Base):
    __tablename__ = 'alias'
    alias = Column(String(250), primary_key=True)
    name = Column(String(250), nullable=False)
    generator = Column(String(250))
    approved = Column(Boolean)

    def __repr__(self):
        return "<Alias(name=%s, alias='%s', generator=%s)>" % (
            self.name, self.alias, self.generator)


class Page(Base):
    __tablename__ = 'page'
    id = Column(Integer, primary_key=True, autoincrement=True)
    url = Column(String(250), nullable=False, unique=True)
    ts = Column(DateTime, nullable=False)
    #ranks = relationship("Ranks", order_by="Ranks.id", backref="page")

    def __repr__(self):
        return "<Page(id=%s, url='%s', ts=%s)>" % (
            self.id, self.url, str(self.ts))



class Ranks(Base):
    __tablename__ = 'ranks'
    id = Column(Integer, primary_key=True, autoincrement=True)
    page_id = Column(Integer, ForeignKey('page.id'), primary_key=True)
    rank = Column(Integer, nullable=False)
    pair = Column(Integer, nullable=False)
    score = Column(Float, nullable=False)
    percentage = Column(Float, nullable=False)
    tie = Column(Integer)
    name1 = Column(String(250), nullable=False)
    name2 = Column(String(250), nullable=False)
    name3 = Column(String(250))
    #page = relationship("Page", backref=backref('page', order_by=id))

    def __repr__(self):
        return "<Rank(id=%s, page_id=%s, name1='%s', name2='%s', name3='%s', score=%s, percentage=%s, rank=%s, tie='%s')>" % (
            self.id, self.page_id, self.name1, self.name2, self.name3, self.score, self.percentage, self.rank, self.tie)


if __name__ == '__main__':
    pass