from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from .repository import cat_fact_repository
from .schema import CatFactCreate, CatFactUpdate, CatFactResponse, CatFactStatsResponse
from .models import CatFact

class CatFactService:
    def __init__(self):
        self.repository = cat_fact_repository

    async def create_fact(self, db: AsyncSession, fact_in: CatFactCreate) -> CatFactResponse:
        """Create a new cat fact"""
        return await self.repository.create(db, fact_in)

    async def get_all_facts(self, db: AsyncSession, skip: int = 0, limit: int = 100) -> List[CatFactResponse]:
        """Get all cat facts with pagination"""
        facts = await self.repository.get_all(db, skip, limit)
        return [CatFactResponse.from_orm(fact) for fact in facts]

    async def get_fact_by_id(self, db: AsyncSession, fact_id: int) -> Optional[CatFactResponse]:
        """Get cat fact by ID"""
        fact = await self.repository.get_by_id(db, fact_id)
        return CatFactResponse.from_orm(fact) if fact else None

    async def update_fact(self, db: AsyncSession, fact_id: int, fact_in: CatFactUpdate) -> Optional[CatFactResponse]:
        """Update cat fact"""
        fact = await self.repository.get_by_id(db, fact_id)
        if fact:
            updated_fact = await self.repository.update(db, fact, fact_in)
            return CatFactResponse.from_orm(updated_fact)
        return None

    async def delete_fact(self, db: AsyncSession, fact_id: int) -> bool:
        """Delete cat fact"""
        return await self.repository.delete(db, fact_id)

    async def get_statistics(self, db: AsyncSession) -> Optional[CatFactStatsResponse]:
        """Get cat facts statistics"""
        stats = await self.repository.get_stats(db)
        return CatFactStatsResponse.from_orm(stats) if stats else None

cat_fact_service = CatFactService()
