from sqlalchemy import Column, Index, String, Text
from sqlalchemy.dialects.mysql.types import TINYINT, INTEGER
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Content(Base):
    __tablename__ = 'tbl_content'
    __table_args__ = (
        Index('id_option', 'id_option', 'name', unique=True),
    )

    id_content = Column(INTEGER(11), primary_key=True)
    id_option = Column(INTEGER(11), nullable=False)
    name = Column(String(100, 'utf8mb4_unicode_ci'), nullable=False)
    position = Column(INTEGER(11), nullable=False)
    active = Column(TINYINT(1), nullable=False)


class ContentFill(Base):
    __tablename__ = 'tbl_content_fill'

    id_content_fill = Column(INTEGER(11), primary_key=True)
    id_content = Column(INTEGER(11), nullable=False)
    textOrfile = Column(Text(collation='utf8mb4_unicode_ci'), nullable=False)
    active = Column(TINYINT(1), nullable=False)
    position = Column(INTEGER(11), nullable=False)
    type = Column(TINYINT(4), nullable=False)


class Option(Base):
    __tablename__ = 'tbl_option'

    id_option = Column(INTEGER(11), primary_key=True)
    id_section = Column(INTEGER(11), nullable=False)
    name = Column(String(100, 'utf8mb4_unicode_ci'), nullable=False)
    position = Column(INTEGER(11), nullable=False)
    active = Column(TINYINT(1), nullable=False)


class Section(Base):
    __tablename__ = 'tbl_section'

    id_section = Column(INTEGER(11), primary_key=True)
    name = Column(String(100, 'utf8mb4_unicode_ci'), nullable=False)
    photo = Column(String(191, 'utf8mb4_unicode_ci'), nullable=False)
    position = Column(INTEGER(11), nullable=False)
    active = Column(TINYINT(1), nullable=False)
