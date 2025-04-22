from fastapi import FastAPI, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional
from datetime import date
from database import SessionLocal, engine
import models, schemas
import ast  

models.Base.metadata.create_all(bind=engine)
app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/api/cpes", response_model=schemas.PaginatedResponse)
def get_cpes(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=10, le=100),
    db: Session = Depends(get_db)
):
    offset = (page - 1) * limit
    total = db.query(models.CPE).count()
    cpes = db.query(models.CPE).order_by(models.CPE.id).offset(offset).limit(limit).all()

    for cpe in cpes:
        if isinstance(cpe.reference_links, str):
            try:
                cpe.reference_links = ast.literal_eval(cpe.reference_links)
            except Exception:
                cpe.reference_links = []

    return {
        "page": page,
        "limit": limit,
        "total": total,
        "data": cpes
    }

@app.get("/api/cpes/search", response_model=schemas.PaginatedResponse)
def search_cpes(
    cpe_title: Optional[str] = Query(None),
    cpe_22_uri: Optional[str] = Query(None),
    cpe_23_uri: Optional[str] = Query(None),
    deprecation_date: Optional[date] = Query(None),
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=10, le=100),
    db: Session = Depends(get_db)
):
    query = db.query(models.CPE)

    if cpe_title:
        query = query.filter(models.CPE.cpe_title.ilike(f"%{cpe_title}%"))
    if cpe_22_uri:
        query = query.filter(models.CPE.cpe_22_uri.ilike(f"%{cpe_22_uri}%"))
    if cpe_23_uri:
        query = query.filter(models.CPE.cpe_23_uri.ilike(f"%{cpe_23_uri}%"))

    if deprecation_date:
        query = query.filter(
            (models.CPE.cpe_22_deprecation_date != None) |
            (models.CPE.cpe_23_deprecation_date != None)
        ).filter(
            ((models.CPE.cpe_22_deprecation_date < deprecation_date) |
             (models.CPE.cpe_23_deprecation_date < deprecation_date))
        )

    total = query.count()
    offset = (page - 1) * limit
    cpes = query.order_by(models.CPE.id).offset(offset).limit(limit).all()

    for cpe in cpes:
        if isinstance(cpe.reference_links, str):
            try:
                cpe.reference_links = ast.literal_eval(cpe.reference_links)
            except Exception:
                cpe.reference_links = []

    return {
        "page": page,
        "limit": limit,
        "total": total,
        "data": cpes
    }