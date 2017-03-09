from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Initialize the database
engine = create_engine("sqlite:///tempdb.sqlite")
Base = declarative_base()
Session = sessionmaker(bind=engine)

class Member(Base):
    __tablename__ = "members"

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    royal = Column(Boolean, nullable=False)

Base.metadata.create_all(engine)
