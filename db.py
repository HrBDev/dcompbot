# coding: utf-8
import os
from os.path import join, dirname

from dotenv import load_dotenv
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import Session

from model import Section, Option, Content, ContentFill

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

# connection string
engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.format(
    os.getenv('DB_USER'), os.getenv('DB_PASSWD'), os.getenv('DB_IP'), os.getenv('DB_NAME')
), pool_recycle=3600)
# create SqlAlchemy Session
session = Session(engine)


def get_sections():
    return session.query(Section.id_section, Section.name). \
        order_by(asc(Section.position)). \
        filter(Section.active).all()


def get_options(id_section):
    return session.query(Option.id_option, Option.id_section, Option.name, Option.position) \
        .filter(Option.active, Option.id_section == id_section) \
        .order_by(asc(Option.position)).all()


def get_content(id_option):
    return session.query(Content.id_content, Content.id_option, Content.name) \
        .filter(Content.active, Content.id_option == id_option) \
        .order_by(asc(Content.position)).all()


def get_content_filled(id_content):
    return session.query(ContentFill.type, ContentFill.textOrfile) \
        .filter(ContentFill.active, ContentFill.id_content == id_content) \
        .order_by(asc(ContentFill.position)).all()


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
    return session.query(Content.id_option, Content.name) \
        .filter(Content.active, Content.id_content == id_content) \
        .first()


def _get_option_name(id_option):
    return session.query(Option.id_section, Option.name) \
        .filter(Option.active, Option.id_option == id_option) \
        .first()


def _get_section_name(id_section):
    return session.query(Section.name) \
        .filter(Section.active, Section.id_section == id_section) \
        .first()
