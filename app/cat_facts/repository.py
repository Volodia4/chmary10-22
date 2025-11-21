from sqlalchemy.orm import Session
from typing import List, Optional
from scr.database.base_repository import BaseRepository
from .models import CatFact
from .schema import CatFactCreate, CatFactUpdate


class CatFactRepository(BaseRepository[CatFact]):
    def __init__(self, db: Session):
        super().__init__(CatFact, db)

    def create_cat_fact(self, cat_fact: CatFactCreate) -> CatFact:
        return self.create(cat_fact.model_dump())

    def get_by_fact_length(self, min_length: Optional[int] = None, max_length: Optional[int] = None) -> List[CatFact]:
        query = self.db.query(CatFact)

        if min_length is not None:
            query = query.filter(CatFact.length >= min_length)
        if max_length is not None:
            query = query.filter(CatFact.length <= max_length)

        return query.all()

    def search_facts(self, search_term: str) -> List[CatFact]:
        return self.db.query(CatFact).filter(CatFact.fact.ilike(f"%{search_term}%")).all()
