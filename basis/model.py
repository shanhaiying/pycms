#encoding=utf-8
'''
Blog model defination.
'''

import web
from sqlalchemy import Table, Column, Integer, String, DateTime, TIMESTAMP, Text
from sqlalchemy.dialects.mysql import MEDIUMTEXT
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref, deferred

from common import Base, engine
from common.dbutil import utcnow
from account.model import User
from models.model import Model

class Template(Base):
    __tablename__ = 'template'
    id = Column(Integer, primary_key=True)
    name = Column(String(32), nullable=False)
    index_file = Column(String(100), nullable=False)
    list_file = Column(String(100), nullable=False)
    display_file = Column(String(100), nullable=False)

    def __repr__(self):
        return "<Template('%s')>" % (self.name)

'''category_article_asso_table = Table('category_article_asso', Base.metadata,
    Column('category_id', Integer, ForeignKey('category.id'), primary_key=True),
    Column('article_id', Integer, ForeignKey('article.id'), primary_key=True)
)
'''

class Category(Base):
    __tablename__ = 'category'
    id = Column(Integer, primary_key=True)
    name = Column(String(64), nullable=False)
    slug = Column(String(32), nullable=False)
    model_id = Column(Integer, ForeignKey('model.id'))
    parent_id = Column(Integer, ForeignKey('category.id'))

    children = relationship("Category", order_by=id, cascade='delete', backref=backref('parent', remote_side=[id]))
    #articles = relationship("Article", secondary=category_article_asso_table, backref=backref('categories'))
    model = relationship(Model, backref=backref('categories'))

    def __repr__(self):
        return "<Category('%s')>" % (self.name)

'''
class Article(Base):
    __tablename__ = 'article'
    id = Column(Integer, primary_key=True)
    title = Column(String(64))
    summary = deferred(Column(Text), group='content')
    content = deferred(Column(MEDIUMTEXT), group='content')
    keywords = Column(String(64))
    thumb = Column(String(100))
    posted_time = Column(TIMESTAMP, default=utcnow())
    updated_time = Column(TIMESTAMP, default=utcnow())
    user_id = Column(Integer, ForeignKey('user.id'))

    user = relationship("User", backref=backref('articles', order_by=id))

    def __unicode__(self):
        return "<Article('%s')>" % (self.title)
'''

template_table = Template.__table__
category_table = Category.__table__
metadata = Base.metadata

#category_table.extend_existing

if __name__ == "__main__":
    metadata.create_all(engine)
