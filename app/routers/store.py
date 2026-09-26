from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .. import models, schemas
from ..database import get_db
from ..utils import standard_response

router = APIRouter(
    prefix="/stores",
    tags=["stores"]
)

from fastapi.responses import JSONResponse

@router.post("/{retailer_id}", response_model=dict, status_code=status.HTTP_201_CREATED)
def create_store(retailer_id: int, store: schemas.StoreCreate, db: Session = Depends(get_db)):
    retailer = db.query(models.Retailer).filter(models.Retailer.id == retailer_id).first()
    if not retailer:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content=standard_response(success=False, error="Retailer not found")
        )

    new_store = models.Store(**store.model_dump(), retailer_id=retailer_id)
    db.add(new_store)
    try:
        db.commit()
        db.refresh(new_store)
        return standard_response(success=True, data=schemas.StoreOut.model_validate(new_store).model_dump())
    except Exception as e:
        db.rollback()
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=standard_response(success=False, error=str(e))
        )

@router.get("/{store_id}", response_model=dict)
def get_store(store_id: int, db: Session = Depends(get_db)):
    store = db.query(models.Store).filter(models.Store.id == store_id).first()
    if not store:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content=standard_response(success=False, error="Store not found")
        )

    return standard_response(success=True, data=schemas.StoreOut.model_validate(store).model_dump())

@router.get("/retailer/{retailer_id}", response_model=dict)
def get_stores_by_retailer(retailer_id: int, db: Session = Depends(get_db)):
    stores = db.query(models.Store).filter(models.Store.retailer_id == retailer_id).all()
    return standard_response(success=True, data=[schemas.StoreOut.model_validate(s).model_dump() for s in stores])
