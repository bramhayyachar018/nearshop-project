from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .. import models, schemas
from ..database import get_db
from ..utils import standard_response

router = APIRouter(
    prefix="/retailers",
    tags=["retailers"]
)

from fastapi.responses import JSONResponse

@router.post("/", response_model=dict, status_code=status.HTTP_201_CREATED)
def create_retailer(retailer: schemas.RetailerCreate, db: Session = Depends(get_db)):
    db_retailer = db.query(models.Retailer).filter(models.Retailer.email == retailer.email).first()
    if db_retailer:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=standard_response(success=False, error="Email already registered")
        )

    new_retailer = models.Retailer(**retailer.model_dump())
    db.add(new_retailer)
    try:
        db.commit()
        db.refresh(new_retailer)
        return standard_response(success=True, data=schemas.RetailerOut.model_validate(new_retailer).model_dump())
    except Exception as e:
        db.rollback()
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=standard_response(success=False, error=str(e))
        )


@router.get("/{retailer_id}", response_model=dict)
def get_retailer(retailer_id: int, db: Session = Depends(get_db)):
    retailer = db.query(models.Retailer).filter(models.Retailer.id == retailer_id).first()
    if not retailer:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content=standard_response(success=False, error="Retailer not found")
        )

    return standard_response(success=True, data=schemas.RetailerOut.model_validate(retailer).model_dump())
