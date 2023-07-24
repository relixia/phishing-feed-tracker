from sqlalchemy import create_engine, Column, String, Boolean, Integer
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class URL(Base):
    __tablename__ = "urls"

    id = Column(String, primary_key=True)
    url = Column(String)
    is_active = Column(Boolean, default=True)

class WebsiteInfo(Base):
    __tablename__ = "website_info"

    id = Column(Integer, primary_key=True, autoincrement=True)
    usom_latest_url = Column(String)
    usom_count = Column(Integer, default=0)
    phishtank_latest_url = Column(String)
    phishtank_count = Column(Integer, default=0)
    openphish_latest_url = Column(String)
    openphish_count = Column(Integer, default=0)
    phishstats_latest_url = Column(String)
    phishstats_count = Column(Integer, default=0)