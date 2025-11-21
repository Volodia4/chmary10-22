from sqlalchemy import Column, Integer, String, Text
from src.database.base import Base, UpdatedMix

class CatFact(Base, UpdatedMix):
    __tablename__ = "cat_facts"

    id = Column(Integer, primary_key=True, index=True)
    fact = Column(Text, nullable=False)
    length = Column(Integer, nullable=False)

class CatFactStats(Base, UpdatedMix):
    __tablename__ = "cat_fact_stats"

    id = Column(Integer, primary_key=True, index=True)
    total_facts = Column(Integer, default=0)
    average_length = Column(Integer, default=0)
    longest_fact = Column(Integer, default=0)
    shortest_fact = Column(Integer, default=0)
