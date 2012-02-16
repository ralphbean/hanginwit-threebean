# -*- coding: utf-8 -*-
"""Sample model module."""

from sqlalchemy import *
from sqlalchemy.orm import mapper, relation
from sqlalchemy import Table, ForeignKey, Column
from sqlalchemy.types import Integer, Unicode, DateTime
from sqlalchemy.orm import relation, backref

from datetime import datetime

from tg2app.model import DeclarativeBase, metadata, DBSession

friends_mapping = Table(
    'friends_mapping', metadata,
    Column('left_id', Integer,
           ForeignKey('fbusers.id'), primary_key=True),
    Column('right_id', Integer,
           ForeignKey('fbusers.id'), primary_key=True))

class FBUser(DeclarativeBase):
    __tablename__ = 'fbusers'

    id = Column(Integer, primary_key=True)
    name = Column(Unicode(255), nullable=False)

    def __unicode__(self):
        return self.name

FBUser.__mapper__.add_property('friends', relation(
    FBUser,
    primaryjoin=FBUser.id==friends_mapping.c.left_id,
    secondaryjoin=friends_mapping.c.right_id==FBUser.id,
    secondary=friends_mapping,
    backref=backref('friends_2')
))


class Login(DeclarativeBase):
    __tablename__ = 'logins'

    id = Column(Integer, primary_key=True)
    name = Column(Unicode(255), nullable=False)
    access_token = Column(Unicode(255), nullable=False)
    last_seen = Column(DateTime, nullable=False)

    def __json__(self):
        return {
            'name': self.name,
        }

class Message(DeclarativeBase):
    __tablename__ = 'messages'

    id = Column(Integer, primary_key=True)
    msg = Column(Unicode(255), nullable=False)
    created_on = Column(DateTime, nullable=False, default=datetime.now)

    def __json__(self):
        return {
            'msg': self.msg,
        }
