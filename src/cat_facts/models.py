from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func
from scr.database.base import Base

class CatFact(Base):
    __tablename__ = "cat_facts"

    id = Column(Integer, primary_key=True, index=True)
    fact = Column(Text, nullable=False)
    length = Column(Integer, nullable=False)
    source = Column(String(100), default="catfact.ninja")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def __repr__(self):
        return f"<CatFact(id={self.id}, fact='{self.fact[:50]}...')>"
