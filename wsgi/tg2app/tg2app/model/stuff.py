# -*- coding: utf-8 -*-
"""Sample model module."""

from sqlalchemy import *
from sqlalchemy.orm import mapper, relation
from sqlalchemy import Table, ForeignKey, Column
from sqlalchemy.types import Integer, Unicode, DateTime
#from sqlalchemy.orm import relation, backref

from datetime import datetime

from tg2app.model import DeclarativeBase, metadata, DBSession


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
