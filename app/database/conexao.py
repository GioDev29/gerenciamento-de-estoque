from sqlalchemy import create_engine
from sqlalchemy.orm import relationship, sessionmaker, declarative_base

engine = create_engine("sqlite:///estoque.db")
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()