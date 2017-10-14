from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Source, Property
from config import *

engine = create_engine(SQLALCHEMY_DATABASE_URI)

Session = sessionmaker()
Session.configure(bind = engine)

s = Session()

def add_source(name, url):
	source = Source(name=name, url=url)
	s.add(source)
	s.commit()

def get_source_by_id(source_id):
	source = s.query(Source).filter_by(id=source_id).first()
	return source

def get_source_by_name(name):
	source = s.query(Source).filter_by(name=name).first()
	return source

def get_all_sources():
	sources = s.query(Source).all()
	return sources

def add_property(name, source, url, localization, content, price):
	prop = Property(name=name, source=source, url=url, localization=localization, content=content, price=price)
	try:
            s.add(prop)
            s.commit()
        except Exception, e:
            s.rollback()
            print "[ERROR] Error (%s)" % e

def get_property_by_id(id):
	prop = s.query(Property).filter_by(id=id).first()
	return prop

def get_property_by_name(name):
	prop = s.query(Property).filter_by(name=name).first()
	return prop

def get_all_properties(limit=None):
	if limit is None:
		props = s.query(Property).all()
	else:
		props = s.query(Property).limit(limit).all()
	return props

def get_properties_data(limit=None):
	props = get_all_properties(limit)
	ids = [p.id for p in props]
	# print ids
	addresses = [p.content for p in props]
	data = {
		'ids': ids,
		'addresses': addresses
	}
	return data

