from sqlalchemy import create_engine, Column, String, Boolean
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class URL(Base):
    __tablename__ = "urls"

    id = Column(String, primary_key=True)
    url = Column(String)
    is_active = Column(Boolean, default=True)
