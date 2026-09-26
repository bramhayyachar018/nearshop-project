from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from .. import models, schemas
from ..database import get_db
from ..utils import standard_response

router = APIRouter(
    prefix="/products",
    tags=["products"]
)

from fastapi.responses import JSONResponse

@router.post("/", response_model=dict, status_code=status.HTTP_201_CREATED)
def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db)):
    new_product = models.Product(**product.model_dump())
    db.add(new_product)
    try:
        db.commit()
        db.refresh(new_product)
        return standard_response(success=True, data=schemas.ProductOut.model_validate(new_product).model_dump())
    except Exception as e:
        db.rollback()
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=standard_response(success=False, error=str(e))
        )


@router.get("/{product_id}", response_model=dict)
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if not product:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content=standard_response(success=False, error="Product not found")
        )

    return standard_response(success=True, data=schemas.ProductOut.model_validate(product).model_dump())
