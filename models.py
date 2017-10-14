# -*- coding: utf-8 -*-
from sqlalchemy import Column, DateTime, String, Integer, Float, Text, ForeignKey, func
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config import *

Base = declarative_base()

class Source(Base):
	__tablename__ = 'source'

	id = Column(Integer, primary_key=True)
	name = Column(String(255), nullable=False)
	url = Column(String(255), nullable=False)

	def __repr__(self):
		return "Source [%d]: (name=%s, url=%s)" % (self.id, self.name, self.url)

class Property(Base):
	__tablename__ = 'property'

	id = Column(Integer, primary_key=True)
	name = Column(String(255), nullable=False)
	source_id = Column(Integer, ForeignKey('source.id'))
	url = Column(String(255), nullable=False)
	localization = Column(String(255))
	content = Column(String(8000))
	price = Column(Float)

	source = relationship(Source, backref=backref('properties', uselist=True))

	def __repr__(self):
		return 'Property [%d]: name=%s, source=<%s>, localization=%s' % (self.id, self.name, self.source, self.localization)

def create_db():
	engine = create_engine(SQLALCHEMY_DATABASE_URI)

	session = sessionmaker()
	session.configure(bind = engine)

	Base.metadata.drop_all(engine)
	Base.metadata.create_all(engine)