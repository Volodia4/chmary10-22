import requests
from typing import List, Optional
from sqlalchemy.orm import Session
from .repository import CatFactRepository
from .schema import CatFactCreate, CatFactResponse
from .config import cat_facts_config
from .models import CatFact


class CatFactService:
    def __init__(self, db: Session):
        self.repository = CatFactRepository(db)
        self.api_url = cat_facts_config.api_url
        self.timeout = cat_facts_config.timeout

    def fetch_from_external_api(self) -> CatFactCreate:
        """Fetch random cat fact from external API"""
        try:
            response = requests.get(self.api_url, timeout=self.timeout)
            response.raise_for_status()
            data = response.json()

            return CatFactCreate(
                fact=data['fact'],
                length=data['length']
            )
        except requests.RequestException as e:
            raise Exception(f"Failed to fetch from external API: {str(e)}")

    def create_cat_fact(self, cat_fact: CatFactCreate) -> CatFact:
        """Create a new cat fact in database"""
        return self.repository.create_cat_fact(cat_fact)

    def get_cat_fact(self, id: int) -> Optional[CatFact]:
        """Get cat fact by ID"""
        return self.repository.get_by_id(id)

    def get_all_cat_facts(self, skip: int = 0, limit: int = 100) -> List[CatFact]:
        """Get all cat facts with pagination"""
        return self.repository.get_all(skip=skip, limit=limit)

    def fetch_and_save_fact(self) -> CatFact:
        """Fetch from external API and save to database"""
        external_fact = self.fetch_from_external_api()
        return self.create_cat_fact(external_fact)

    def get_facts_by_length(self, min_length: Optional[int] = None, max_length: Optional[int] = None) -> List[CatFact]:
        """Get facts filtered by length"""
        return self.repository.get_by_fact_length(min_length, max_length)

    def search_facts(self, search_term: str) -> List[CatFact]:
        """Search facts by text content"""
        return self.repository.search_facts(search_term)

    def get_facts_count(self) -> int:
        """Get total number of facts in database"""
        return self.repository.count()
