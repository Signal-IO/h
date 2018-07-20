"""
Add the __default__ organization if it doesn't already exist.

Revision ID: 8a7f31c4525d
Revises: 46a22db075d5
Create Date: 2018-03-27 16:50:20.959215

"""
from __future__ import unicode_literals

import logging

from alembic import op
import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

revision = '8a7f31c4525d'
down_revision = '46a22db075d5'


log = logging.getLogger(__name__)


Base = declarative_base()
Session = sessionmaker()


H_LOGO = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 91.69845580995576" xmlns:xlink="http://www.w3.org/1999/xlink" version="1.1"  ><g transform="translate(-6.254654733789473 -11.603213424607366) scale(1.1283879639420678)" id="containerlessSvgTemplate"><g fill="#406BFF"><path d="M60.756 10.283H40.335L5.543 50.874l34.945 40.674h20.724L25.963 50.874z"></path><path d="M73.758 23.519l-5.641-7.088-29.659 34.443 29.659 34.444 5.641-7.088-23.719-27.356z"></path><path d="M81.86 36.918l-11.708 13.5 11.708 13.5 12.305-13.5z"></path></g></g></svg>"""


class Group(Base):
    __tablename__ = 'group'

    id = sa.Column(sa.Integer, primary_key=True)
    pubid = sa.Column(sa.Text())
    authority = sa.Column(sa.UnicodeText())


class Organization(Base):
    __tablename__ = 'organization'
    id = sa.Column(sa.Integer, primary_key=True)
    pubid = sa.Column(sa.Text, unique=True)
    name = sa.Column(sa.UnicodeText, index=True)
    logo = sa.Column(sa.UnicodeText)
    authority = sa.Column(sa.UnicodeText)


def upgrade():
    session = Session(bind=op.get_bind())

    default_org = session.query(Organization).filter_by(pubid='__default__').one_or_none()
    if default_org:
        log.info("__default__ organization already exists, not creating it")
        return

    log.info("__default__ organization doesn't exist yet, creating it")
    authority = session.query(Group).filter_by(pubid='__world__').one().authority
    session.add(Organization(name='Hypothesis',
                             logo=H_LOGO,
                             pubid='__default__',
                             authority=authority,
                             ))
    session.commit()


def downgrade():
    # Don't try to delete the __default__ organization when downgrading
    # because there might be groups that are related to it.
    pass
