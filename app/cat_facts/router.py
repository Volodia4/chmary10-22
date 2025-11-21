from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import List, Optional

from scr.database.utils import get_db
from .service import CatFactService
from .schema import CatFactResponse, CatFactListResponse

router = APIRouter(prefix="/cat-facts", tags=["Cat Facts Database"])


@router.post("/fetch-external", response_model=CatFactResponse, status_code=status.HTTP_201_CREATED)
def fetch_and_save_external_fact(
        db: Session = Depends(get_db)
):
    """Fetch a random cat fact from external API and save to database"""
    try:
        service = CatFactService(db)
        fact = service.fetch_and_save_fact()
        return fact
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch and save fact: {str(e)}"
        )


@router.get("/", response_model=CatFactListResponse)
def get_all_facts(
        skip: int = Query(0, ge=0, description="Number of records to skip"),
        limit: int = Query(100, ge=1, le=1000, description="Number of records to return"),
        db: Session = Depends(get_db)
):
    """Get all cat facts from database with pagination"""
    service = CatFactService(db)
    facts = service.get_all_cat_facts(skip=skip, limit=limit)
    total = service.get_facts_count()

    return CatFactListResponse(
        items=facts,
        total=total,
        page=skip // limit + 1 if limit > 0 else 1,
        size=limit
    )


@router.get("/{fact_id}", response_model=CatFactResponse)
def get_fact_by_id(
        fact_id: int,
        db: Session = Depends(get_db)
):
    """Get specific cat fact by ID"""
    service = CatFactService(db)
    fact = service.get_cat_fact(fact_id)

    if not fact:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Cat fact with ID {fact_id} not found"
        )

    return fact


@router.get("/search/by-length", response_model=CatFactListResponse)
def get_facts_by_length(
        min_length: Optional[int] = Query(None, ge=1, description="Minimum fact length"),
        max_length: Optional[int] = Query(None, ge=1, description="Maximum fact length"),
        db: Session = Depends(get_db)
):
    """Get facts filtered by text length"""
    service = CatFactService(db)
    facts = service.get_facts_by_length(min_length, max_length)

    return CatFactListResponse(
        items=facts,
        total=len(facts),
        page=1,
        size=len(facts)
    )


@router.get("/search/text", response_model=CatFactListResponse)
def search_facts(
        query: str = Query(..., min_length=2, description="Search term"),
        db: Session = Depends(get_db)
):
    """Search facts by text content"""
    service = CatFactService(db)
    facts = service.search_facts(query)

    return CatFactListResponse(
        items=facts,
        total=len(facts),
        page=1,
        size=len(facts)
    )
