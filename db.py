# coding: utf-8
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import Session

from model import TblSection, TblOption, TblContent, TblContentFill

# connection string
engine = create_engine('mysql+mysqldb://<DB_USER>:<DB_PASSWD>@<DB_IO>/<DB_NAME>', pool_recycle=3600)
# create SqlAlchemy Session
session = Session(engine)


def get_sections():
    return session.query(TblSection.id_section, TblSection.name). \
        order_by(asc(TblSection.position)). \
        filter(TblSection.active).all()


def get_options(id_section):
    return session.query(TblOption.id_option, TblOption.id_section, TblOption.name, TblOption.position) \
        .filter(TblOption.active, TblOption.id_section == id_section) \
        .order_by(asc(TblOption.position)).all()


def get_content(id_option):
    return session.query(TblContent.id_content, TblContent.id_option, TblContent.name) \
        .filter(TblContent.active, TblContent.id_option == id_option) \
        .order_by(asc(TblContent.position)).all()


def get_content_filled(id_content):
    return session.query(TblContentFill.type, TblContentFill.textOrfile) \
        .filter(TblContentFill.active, TblContentFill.id_content == id_content) \
        .order_by(asc(TblContentFill.position)).all()


def get_path_content(id_option):
    option = _get_option_name(id_option)
    section = _get_section_name(option[0])
    path = section[0] + " -> " + option[1]
    return path


def get_path_content_filled(id_content):
    content = _get_content_name(id_content)
    option = _get_option_name(content[0])
    section = _get_section_name(option[0])
    path = section[0] + " -> " + option[1] + " -> " + content[1]
    return path


def _get_content_name(id_content):
    return session.query(TblContent.id_option, TblContent.name) \
        .filter(TblContent.active, TblContent.id_content == id_content) \
        .first()


def _get_option_name(id_option):
    return session.query(TblOption.id_section, TblOption.name) \
        .filter(TblOption.active, TblOption.id_option == id_option) \
        .first()


def _get_section_name(id_section):
    return session.query(TblSection.name) \
        .filter(TblSection.active, TblSection.id_section == id_section) \
        .first()
