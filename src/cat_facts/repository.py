from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func
from typing import List, Optional
from src.database.base_repository import BaseRepository
from .models import CatFact, CatFactStats
from .schema import CatFactCreate, CatFactUpdate


class CatFactRepository(BaseRepository[CatFact, CatFactCreate, CatFactUpdate]):
    def __init__(self):
        super().__init__(CatFact)

    async def get_stats(self, db: AsyncSession) -> Optional[CatFactStats]:
        """Get cat facts statistics"""
        result = await db.execute(
            func.avg(CatFact.length).label('avg_length'),
            func.max(CatFact.length).label('max_length'),
            func.min(CatFact.length).label('min_length'),
            func.count(CatFact.id).label('total')
        )
        stats = result.first()

        if stats:
            return CatFactStats(
                total_facts=stats.total or 0,
                average_length=round(stats.avg_length or 0, 2),
                longest_fact=stats.max_length or 0,
                shortest_fact=stats.min_length or 0
            )
        return None


cat_fact_repository = CatFactRepository()
