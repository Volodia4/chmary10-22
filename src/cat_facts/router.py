from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from src.database.utils import get_db
from .schema import CatFactCreate, CatFactUpdate, CatFactResponse, CatFactStatsResponse
from .service import cat_fact_service

router = APIRouter(prefix="/facts", tags=["Cat Facts"])

@router.post("/", response_model=CatFactResponse, status_code=status.HTTP_201_CREATED)
async def create_fact(
    fact_in: CatFactCreate,
    db: AsyncSession = Depends(get_db)
):
    """Create a new cat fact"""
    return await cat_fact_service.create_fact(db, fact_in)

@router.get("/", response_model=List[CatFactResponse])
async def get_all_facts(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db)
):
    """Get all cat facts"""
    return await cat_fact_service.get_all_facts(db, skip, limit)

@router.get("/{fact_id}", response_model=CatFactResponse)
async def get_fact(
    fact_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Get cat fact by ID"""
    fact = await cat_fact_service.get_fact_by_id(db, fact_id)
    if not fact:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cat fact not found"
        )
    return fact

@router.put("/{fact_id}", response_model=CatFactResponse)
async def update_fact(
    fact_id: int,
    fact_in: CatFactUpdate,
    db: AsyncSession = Depends(get_db)
):
    """Update cat fact"""
    fact = await cat_fact_service.update_fact(db, fact_id, fact_in)
    if not fact:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cat fact not found"
        )
    return fact

@router.delete("/{fact_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_fact(
    fact_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Delete cat fact"""
    success = await cat_fact_service.delete_fact(db, fact_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cat fact not found"
        )

@router.get("/stats/statistics", response_model=CatFactStatsResponse)
async def get_statistics(db: AsyncSession = Depends(get_db)):
    """Get cat facts statistics"""
    stats = await cat_fact_service.get_statistics(db)
    if not stats:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No statistics available"
        )
    return stats
